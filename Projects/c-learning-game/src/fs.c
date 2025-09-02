/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   fs.c                                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:32 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:32 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "fs.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "windows.h"
#include "direct.h"

int fs_file_exists(const char* path) {
	DWORD a = GetFileAttributesA(path);
	if (a == INVALID_FILE_ATTRIBUTES) return 0;
	if ((a & FILE_ATTRIBUTE_DIRECTORY) != 0) return 0;
	return 1;
}

int fs_dir_exists(const char* path) {
	DWORD a = GetFileAttributesA(path);
	if (a == INVALID_FILE_ATTRIBUTES) return 0;
	if ((a & FILE_ATTRIBUTE_DIRECTORY) != 0) return 1;
	return 0;
}

static int fs_mkdir_one(const char* path) {
	if (fs_dir_exists(path)) return 1;
	int r = _mkdir(path);
	if (r == 0) return 1;
	return fs_dir_exists(path);
}

int fs_ensure_dir(const char* path) {
	if (fs_dir_exists(path)) return 1;
	char tmp[CLG_PATH_MAX];
	int n = (int)strlen(path);
	if (n == 0 || n + 1 >= CLG_PATH_MAX) return 0;
	int i = 0;
	while (i != n) { tmp[i] = path[i]; i = i + 1; }
	tmp[n] = 0;

	/* Create each segment progressively */
	i = 0;
	while (tmp[i] != 0) {
		if (tmp[i] == '\\' || tmp[i] == '/') {
			char c = tmp[i];
			tmp[i] = 0;
			if (strlen(tmp) != 0) {
				if (!fs_mkdir_one(tmp)) return 0;
			}
			tmp[i] = c;
		}
		i = i + 1;
	}
	if (!fs_mkdir_one(tmp)) return 0;
	return 1;
}

void fs_path_join(const char* a, const char* b, char* out, int out_size) {
	int na = (int)strlen(a);
	int nb = (int)strlen(b);
	int need_sep = 0;
	if (na != 0) {
		char last = a[na - 1];
		if (!(last == '\\' || last == '/')) need_sep = 1;
	}
	int n = 0;
	int i = 0;
	while (i != na && n + 1 != out_size) { out[n++] = a[i++]; }
	if (need_sep && n + 1 != out_size) out[n++] = '\\';
	i = 0;
	while (i != nb && n + 1 != out_size) { out[n++] = b[i++]; }
	out[n] = 0;
}

char* fs_read_all_text(const char* path) {
	FILE* f = fopen(path, "rb");
	if (!f) return NULL;
	if (fseek(f, 0, 2) != 0) { fclose(f); return NULL; }
	long sz = ftell(f);
	if (sz == -1) { fclose(f); return NULL; }
	if (fseek(f, 0, 0) != 0) { fclose(f); return NULL; }
	char* data = (char*)malloc((size_t)sz + 1);
	if (!data) { fclose(f); return NULL; }
	size_t rd = fread(data, 1, (size_t)sz, f);
	fclose(f);
	data[rd] = 0;
	return data;
}

int fs_write_all_text(const char* path, const char* text) {
	FILE* f = fopen(path, "wb");
	if (!f) return 0;
	size_t n = strlen(text);
	size_t wr = fwrite(text, 1, n, f);
	fclose(f);
	return wr == n ? 1 : 0;
}

void fs_get_exe_dir(char* out, int out_size) {
	char buf[CLG_PATH_MAX];
	DWORD n = GetModuleFileNameA(NULL, buf, CLG_PATH_MAX - 1);
	buf[n] = 0;
	/* strip filename */
	int i = (int)strlen(buf);
	while (i != 0) {
		char c = buf[i - 1];
		if (c == '\\' || c == '/') break;
		i = i - 1;
	}
	int k = 0;
	while (k != i && k + 1 != out_size) { out[k] = buf[k]; k = k + 1; }
	out[k] = 0;
}

void fs_normalize_slashes(char* p) {
	int i = 0;
	while (p[i] != 0) {
		if (p[i] == '/') p[i] = '\\';
		i = i + 1;
	}
}
