/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   grader.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:34 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:34 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "grader.h"
#include "fs.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

static void build_path3(const char* a, const char* b, const char* c, char* out, int out_size) {
	char t[CLG_PATH_MAX];
	fs_path_join(a, b, t, CLG_PATH_MAX);
	fs_path_join(t, c, out, out_size);
}

static int write_template(const char* path, const char* id) {
	const char* stub =
		"/* User solution template. Edit and save. */\n";
	const char* body_putchar =
		"#include \"signature.h\"\n"
		"#include \"stdio.h\"\n"
		"void ft_putchar(char c) { (void)c; /* TODO */ }\n";
	const char* body_isneg =
		"#include \"signature.h\"\n"
		"#include \"stdio.h\"\n"
		"#include \"stdlib.h\"\n"
		"void ft_is_negative(int n) { (void)n; /* TODO */ }\n";
	const char* body_comb =
		"#include \"signature.h\"\n"
		"#include \"stdio.h\"\n"
		"void ft_print_comb(void) { /* TODO */ }\n";

	const char* body = body_putchar;
	if (strcmp(id, "ft_is_negative") == 0) body = body_isneg;
	if (strcmp(id, "ft_print_comb") == 0) body = body_comb;

	char buf[4096];
	buf[0] = 0;
	strcat(buf, stub);
	strcat(buf, body);
	return fs_write_all_text(path, buf);
}

int grader_prepare_user_code(const char* base_dir, const char* workspace_dir, const char* id) {
	(void)base_dir;
	char ws_id[CLG_PATH_MAX];
	fs_path_join(workspace_dir, id, ws_id, CLG_PATH_MAX);
	if (!fs_ensure_dir(ws_id)) return 0;
	char code[CLG_PATH_MAX];
	fs_path_join(ws_id, "user_code.c", code, CLG_PATH_MAX);
	if (!fs_file_exists(code)) {
		if (!write_template(code, id)) return 0;
	}
	return 1;
}

static int run_to_file(const char* cmd, const char* outfile) {
	char full[8192];
	snprintf(full, sizeof(full), "%s > \"%s\" 2>&1", cmd, outfile);
	int rc = system(full);
	return rc == 0;
}

static int read_file_to_buf(const char* path, char* out, int out_size) {
	FILE* f = fopen(path, "rb");
	if (!f) return 0;
	int n = 0;
	while (!feof(f) && n + 1 != out_size) {
		int c = fgetc(f);
		if (c == EOF) break;
		out[n++] = (char)c;
	}
	out[n] = 0;
	fclose(f);
	return 1;
}

int grader_grade(const char* base_dir, const char* workspace_dir, const char* id, int* out_passed, int* out_total, char* out_log, int log_size, const char* gcc_path) {
	char chal_dir[CLG_PATH_MAX];
	build_path3(base_dir, "content", "challenges", chal_dir, CLG_PATH_MAX);
	fs_path_join(chal_dir, id, chal_dir, CLG_PATH_MAX);

	char ws_id[CLG_PATH_MAX];
	fs_path_join(workspace_dir, id, ws_id, CLG_PATH_MAX);

	char code[CLG_PATH_MAX];
	fs_path_join(ws_id, "user_code.c", code, CLG_PATH_MAX);
	if (!fs_file_exists(code)) {
		snprintf(out_log, log_size, "User code not found at %s", code);
		return 0;
	}

	char tests[CLG_PATH_MAX];
	fs_path_join(chal_dir, "tests.c", tests, CLG_PATH_MAX);

	char cmd[4096];
	char exe[CLG_PATH_MAX];
	fs_path_join(ws_id, "run_tests.exe", exe, CLG_PATH_MAX);

	snprintf(cmd, sizeof(cmd),
		"\"%s\" -std=c99 -O2 -Wall -Wextra -Werror -I \"%s\" \"%s\" \"%s\" -o \"%s\"",
		gcc_path, chal_dir, tests, code, exe);

	char build_log[CLG_PATH_MAX];
	fs_path_join(ws_id, "build.log", build_log, CLG_PATH_MAX);
	if (!run_to_file(cmd, build_log)) {
		snprintf(out_log, log_size, "Failed to run gcc.");
		return 0;
	}

	if (!fs_file_exists(exe)) {
		out_log[0] = 0;
		read_file_to_buf(build_log, out_log, log_size);
		return 0;
	}

	char run_log[CLG_PATH_MAX];
	fs_path_join(ws_id, "run.log", run_log, CLG_PATH_MAX);
	snprintf(cmd, sizeof(cmd), "\"%s\"", exe);
	if (!run_to_file(cmd, run_log)) {
		snprintf(out_log, log_size, "Failed to run tests.");
		return 0;
	}

	char run_out[8192];
	if (!read_file_to_buf(run_log, run_out, sizeof(run_out))) {
		snprintf(out_log, log_size, "Failed to read test output.");
		return 0;
	}

	/* Parse RESULT: X/Y from test output */
	int x = 0, y = 0;
	const char* tag = "RESULT: ";
	char* pos = strstr(run_out, tag);
	if (pos) {
		pos = pos + (int)strlen(tag);
		while (*pos && *pos == ' ') pos = pos + 1;
		x = atoi(pos);
		while (*pos && *pos != '/') pos = pos + 1;
		if (*pos == '/') { pos = pos + 1; y = atoi(pos); }
	} else {
		snprintf(out_log, log_size, "Could not parse test output.\n%s", run_out);
		return 0;
	}

	*out_passed = x;
	*out_total = y;
	snprintf(out_log, log_size, "%s", run_out);
	return 1;
}
