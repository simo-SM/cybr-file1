/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   game.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:33 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:33 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "game.h"
#include "ui.h"
#include "fs.h"
#include "content.h"
#include "json.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

static void set_default_paths(GameState* g) {
	fs_get_exe_dir(g->base_dir, CLG_PATH_MAX);
	/* Try to locate content under exe dir first, else project root dev layout */
	char c1[CLG_PATH_MAX];
	fs_path_join(g->base_dir, "content", c1, CLG_PATH_MAX);
	if (fs_dir_exists(c1)) {
		strcpy(g->content_dir, c1);
	} else {
		/* dev layout: ..\content relative to build\ */
		char up[CLG_PATH_MAX];
		strcpy(up, g->base_dir);
		/* strip trailing build\ if present */
		int n = (int)strlen(up);
		if (n != 0 && up[n - 1] == '\\') up[n - 1] = 0;
		char* last = up + strlen(up);
		while (last != up && *(last - 1) != '\\') last = last - 1;
		*last = 0;
		fs_path_join(up, "content", g->content_dir, CLG_PATH_MAX);
	}
	fs_path_join(g->base_dir, "workspace", g->workspace_dir, CLG_PATH_MAX);
	fs_path_join(g->base_dir, "save", g->save_dir, CLG_PATH_MAX);
}

void game_init(GameState* g) {
	memset(g, 0, sizeof(*g));
	set_default_paths(g);
	g->best_score_c_basics = 0;
	strcpy(g->status_putchar, "unknown");
	strcpy(g->status_isneg, "unknown");
	strcpy(g->status_comb, "unknown");
}

static void progress_path(const GameState* g, char* out, int out_size) {
	fs_path_join(g->save_dir, "progress.json", out, out_size);
}

static void ensure_dirs(GameState* g) {
	fs_ensure_dir(g->save_dir);
	fs_ensure_dir(g->workspace_dir);
}

void game_load(GameState* g) {
	ensure_dirs(g);
	char path[CLG_PATH_MAX];
	progress_path(g, path, CLG_PATH_MAX);
	if (!fs_file_exists(path)) {
		return;
	}
	char* t = fs_read_all_text(path);
	if (!t) return;
	/* naive parsing */
	char ws[CLG_PATH_MAX];
	int pos = 0;
	if (json_extract_string(t, "workspace_dir", 0, ws, sizeof(ws), &pos)) {
		strcpy(g->workspace_dir, ws);
		fs_normalize_slashes(g->workspace_dir);
	}
	int best = 0;
	if (json_extract_int(t, "best_score", 0, &best, &pos)) {
		g->best_score_c_basics = best;
	}
	char s[32];
	if (json_extract_string(t, "ft_putchar", 0, s, sizeof(s), &pos)) strcpy(g->status_putchar, s);
	if (json_extract_string(t, "ft_is_negative", 0, s, sizeof(s), &pos)) strcpy(g->status_isneg, s);
	if (json_extract_string(t, "ft_print_comb", 0, s, sizeof(s), &pos)) strcpy(g->status_comb, s);
	free(t);
}

void game_save(const GameState* g) {
	ensure_dirs((GameState*)g);
	char path[CLG_PATH_MAX];
	progress_path(g, path, CLG_PATH_MAX);
	char buf[4096];
	snprintf(buf, sizeof(buf),
		"{\n"
		"  \"workspace_dir\": \"%s\",\n"
		"  \"quizzes\": { \"c_basics\": { \"best_score\": %d } },\n"
		"  \"challenges\": {\n"
		"    \"ft_putchar\": \"%s\",\n"
		"    \"ft_is_negative\": \"%s\",\n"
		"    \"ft_print_comb\": \"%s\"\n"
		"  }\n"
		"}\n",
		g->workspace_dir,
		g->best_score_c_basics,
		g->status_putchar,
		g->status_isneg,
		g->status_comb
	);
	fs_write_all_text(path, buf);
}

static void show_progress(const GameState* g) {
	ui_clear();
	printf("Progress\n");
	ui_print_hr();
	printf("Quiz c_basics best score: %d\n", g->best_score_c_basics);
	printf("Challenge ft_putchar: %s\n", g->status_putchar);
	printf("Challenge ft_is_negative: %s\n", g->status_isneg);
	printf("Challenge ft_print_comb: %s\n", g->status_comb);
	ui_print_hr();
	ui_pause();
}

static void settings_menu(GameState* g) {
	for (;;) {
		ui_clear();
		printf("Settings\n");
		ui_print_hr();
		printf("Current workspace: %s\n", g->workspace_dir);
		ui_print_hr();
		const char* items[] = { "Change workspace directory", "Back" };
		int sel = ui_menu("Settings", items, 2);
		if (sel == 1) return;
		if (sel == 0) {
			printf("Enter new workspace directory path: ");
			char line[CLG_PATH_MAX];
			ui_read_line(line, sizeof(line));
			if (strlen(line) != 0) {
				strcpy(g->workspace_dir, line);
				fs_normalize_slashes(g->workspace_dir);
				if (!fs_ensure_dir(g->workspace_dir)) {
					printf("Failed to create folder: %s\n", g->workspace_dir);
				} else {
					printf("Workspace set to: %s\n", g->workspace_dir);
				}
				ui_pause();
			}
		}
	}
}

void game_main(GameState* g, const char* gcc_path) {
	const char* items[] = {
		"Learn",
		"Quizzes",
		"Code Challenges",
		"Progress",
		"Settings",
		"Exit"
	};
	for (;;) {
		int sel = ui_menu("C Learning Game", items, 6);
		if (sel == 5) {
			game_save(g);
			ui_clear();
			printf("Goodbye.\n");
			return;
		} else if (sel == 0) {
			content_show_topics(g->content_dir);
		} else if (sel == 1) {
			content_run_quiz(g->content_dir, g);
			game_save(g);
		} else if (sel == 2) {
			content_challenges_menu(g->content_dir, g, gcc_path);
			game_save(g);
		} else if (sel == 3) {
			show_progress(g);
		} else if (sel == 4) {
			settings_menu(g);
			game_save(g);
		}
	}
}
