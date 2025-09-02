/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   content.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:31 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:31 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "content.h"
#include "ui.h"
#include "fs.h"
#include "json.h"
#include "grader.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

typedef struct QuizQuestion {
	char id[32];
	char question[512];
	int choice_count;
	char choices[8][256];
	int answer_index;
} QuizQuestion;

static void print_file(const char* path) {
	char* t = fs_read_all_text(path);
	if (!t) {
		printf("Could not read %s\n", path);
		ui_pause();
		return;
	}
	printf("%s\n", t);
	free(t);
	ui_pause();
}

void content_show_topics(const char* content_dir) {
	const char* names[] = {
		"Variables and Types",
		"Control Flow",
		"Functions",
		"Pointers and Memory",
		"Arrays and Strings",
		"Back"
	};
	const char* files[] = {
		"variables.md",
		"control_flow.md",
		"functions.md",
		"pointers_memory.md",
		"arrays_strings.md"
	};
	for (;;) {
		int choice = ui_menu("Learn", names, 6);
		if (choice == 5) return;
		char path[CLG_PATH_MAX];
		char topics[CLG_PATH_MAX];
		fs_path_join(content_dir, "topics", topics, CLG_PATH_MAX);
		fs_path_join(topics, files[choice], path, CLG_PATH_MAX);
		ui_clear();
		print_file(path);
	}
}

static int parse_quiz(const char* path, char* title_out, int title_size, QuizQuestion* qs, int max_q, int* out_count) {
	char* s = fs_read_all_text(path);
	if (!s) return 0;
	int pos = 0;
	if (!json_extract_string(s, "title", 0, title_out, title_size, &pos)) {
		strcpy(title_out, "C Basics");
	}
	/* find questions array start position */
	char tmp_title[64];
	json_extract_string(s, "questions", 0, tmp_title, 1, &pos); /* position at the array value */
	/* Now manually find the array start '[' after "questions" key */
	const char* p = s + pos;
	while (*p && *p != '[') p = p + 1;
	if (!*p) { free(s); return 0; }
	int qcount = 0;
	while (*p && qcount != max_q) {
		if (*p == '{') {
			int item_pos = (int)(p - s);
			QuizQuestion q;
			memset(&q, 0, sizeof(q));
			json_extract_string(s, "id", item_pos, q.id, sizeof(q.id), &item_pos);
			json_extract_string(s, "question", item_pos, q.question, sizeof(q.question), &item_pos);
			json_extract_string_array(s, "choices", item_pos, q.choices, 8, &q.choice_count, &item_pos);
			json_extract_int(s, "answer_index", item_pos, &q.answer_index, &item_pos);
			qs[qcount] = q;
			qcount = qcount + 1;
			/* Move p to end of this object */
			while (*p && *p != '}') p = p + 1;
		}
		if (*p == ']') break;
		p = p + 1;
	}
	*out_count = qcount;
	free(s);
	return qcount != 0;
}

void content_run_quiz(const char* content_dir, GameState* state) {
	char qdir[CLG_PATH_MAX];
	fs_path_join(content_dir, "quizzes", qdir, CLG_PATH_MAX);
	char path[CLG_PATH_MAX];
	fs_path_join(qdir, "c_basics.json", path, CLG_PATH_MAX);

	QuizQuestion qs[32];
	int qn = 0;
	char title[128];
	if (!parse_quiz(path, title, sizeof(title), qs, 32, &qn)) {
		printf("Failed to load quiz at %s\n", path);
		ui_pause();
		return;
	}

	int score = 0;
	int i = 0;
	while (i != qn) {
		ui_clear();
		ui_print_hr();
		printf("%s\n", title);
		ui_print_hr();
		printf("Q%d: %s\n", i + 1, qs[i].question);
		int j = 0;
		while (j != qs[i].choice_count) {
			printf("  %d) %s\n", j + 1, qs[i].choices[j]);
			j = j + 1;
		}
		printf("Your answer: ");
		char line[32];
		ui_read_line(line, sizeof(line));
		int ans_index = -1;
		j = 0;
		while (j != qs[i].choice_count) {
			char num[16];
			sprintf(num, "%d", j + 1);
			if (strcmp(line, num) == 0) { ans_index = j; break; }
			j = j + 1;
		}
		if (ans_index == qs[i].answer_index) {
			printf("Correct!\n");
			score = score + 1;
		} else {
			printf("Wrong. Correct is %d.\n", qs[i].answer_index + 1);
		}
		ui_pause();
		i = i + 1;
	}

	ui_clear();
	printf("Quiz complete. Score: %d of %d\n", score, qn);
	if (score != 0 && score > state->best_score_c_basics) {
		state->best_score_c_basics = score;
		printf("New best score saved.\n");
	}
	ui_pause();
}

static void show_description(const char* chal_dir) {
	char desc[CLG_PATH_MAX];
	fs_path_join(chal_dir, "description.md", desc, CLG_PATH_MAX);
	print_file(desc);
}

void content_challenges_menu(const char* content_dir, GameState* state, const char* gcc_path) {
	const char* items[] = {
		"ft_putchar",
		"ft_is_negative",
		"ft_print_comb",
		"Back"
	};
	for (;;) {
		int choice = ui_menu("Code Challenges", items, 4);
		if (choice == 3) return;
		const char* id = items[choice];
		char chal_dir[CLG_PATH_MAX];
		char cdir[CLG_PATH_MAX];
		fs_path_join(content_dir, "challenges", cdir, CLG_PATH_MAX);
		fs_path_join(cdir, id, chal_dir, CLG_PATH_MAX);

		for (;;) {
			const char* act[] = { "View Description", "Open Template", "Grade", "Back" };
			int act_choice = ui_menu(id, act, 4);
			if (act_choice == 3) break;
			if (act_choice == 0) {
				ui_clear();
				show_description(chal_dir);
			} else if (act_choice == 1) {
				if (!grader_prepare_user_code(content_dir, state->workspace_dir, id)) {
					printf("Failed to prepare template.\n"); ui_pause();
				} else {
					char ws_id[CLG_PATH_MAX];
					fs_path_join(state->workspace_dir, id, ws_id, CLG_PATH_MAX);
					char code[CLG_PATH_MAX];
					fs_path_join(ws_id, "user_code.c", code, CLG_PATH_MAX);
					char cmd[CLG_PATH_MAX * 2];
					snprintf(cmd, sizeof(cmd), "cmd /c start \"\" \"%s\"", code);
					system(cmd);
					printf("Opened: %s\n", code);
					ui_pause();
				}
			} else if (act_choice == 2) {
				if (!grader_prepare_user_code(content_dir, state->workspace_dir, id)) {
					printf("Failed to prepare template.\n"); ui_pause();
				} else {
					int passed = 0, total = 0;
					char log[8192];
					if (!grader_grade(content_dir, state->workspace_dir, id, &passed, &total, log, sizeof(log), gcc_path)) {
						printf("Grade failed:\n%s\n", log);
					} else {
						printf("%s\n", log);
						printf("Score: %d of %d\n", passed, total);
						if (total != 0 && passed == total) {
							if (strcmp(id, "ft_putchar") == 0) strcpy(state->status_putchar, "passed");
							if (strcmp(id, "ft_is_negative") == 0) strcpy(state->status_isneg, "passed");
							if (strcmp(id, "ft_print_comb") == 0) strcpy(state->status_comb, "passed");
						}
					}
					ui_pause();
				}
			}
		}
	}
}
