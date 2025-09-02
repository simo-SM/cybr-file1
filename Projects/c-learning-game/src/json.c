/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   json.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:35 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:35 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "json.h"
#include "stdio.h"
#include "string.h"
#include "ctype.h"

/* Very small helpers that scan for keys and extract simple values.
   Works for the included content format. Not a general JSON parser.
*/

static const char* find_key(const char* s, const char* key, int start_pos) {
	const char* p = s + start_pos;
	int key_len = (int)strlen(key);
	while (*p) {
		if (*p == '"') {
			const char* k = p + 1;
			int i = 0;
			while (k[i] && k[i] != '"') i = i + 1;
			if (i == key_len && strncmp(k, key, key_len) == 0) {
				const char* q = k + i + 1;
				while (*q && *q != ':') q = q + 1;
				if (*q == ':') return q + 1;
			}
			p = k + i;
		}
		p = p + 1;
	}
	return NULL;
}

const char* json_skip_ws(const char* p) {
	while (*p && (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n')) p = p + 1;
	return p;
}

int json_extract_string(const char* src, const char* key, int start_pos, char* out, int out_size, int* out_pos) {
	const char* v = find_key(src, key, start_pos);
	if (!v) return 0;
	v = json_skip_ws(v);
	if (*v != '"') return 0;
	v = v + 1;
	int n = 0;
	while (*v && *v != '"' && n + 1 != out_size) {
		if (*v == '\\') {
			v = v + 1;
			if (!*v) break;
		}
		out[n++] = *v++;
	}
	out[n] = 0;
	if (*v == '"') v = v + 1;
	if (out_pos) *out_pos = (int)(v - src);
	return 1;
}

int json_extract_int(const char* src, const char* key, int start_pos, int* out_value, int* out_pos) {
	const char* v = find_key(src, key, start_pos);
	if (!v) return 0;
	v = json_skip_ws(v);
	int sign = 1;
	if (*v == '-') { sign = -1; v = v + 1; }
	int x = 0;
	int any = 0;
	while (*v && *v >= '0' && *v <= '9') {
		x = x * 10 + (*v - '0');
		v = v + 1;
		any = 1;
	}
	if (!any) return 0;
	*out_value = x * sign;
	if (out_pos) *out_pos = (int)(v - src);
	return 1;
}

int json_extract_string_array(const char* src, const char* key, int start_pos, char items[][256], int max_items, int* out_count, int* out_pos) {
	const char* v = find_key(src, key, start_pos);
	if (!v) return 0;
	v = json_skip_ws(v);
	if (*v != '[') return 0;
	v = v + 1;
	int count = 0;
	for (;;) {
		v = json_skip_ws(v);
		if (*v == ']') { v = v + 1; break; }
		if (*v != '"') return 0;
		v = v + 1;
		int n = 0;
		while (*v && *v != '"' && n + 1 != 256) {
			if (*v == '\\') {
				v = v + 1;
				if (!*v) break;
			}
			items[count][n++] = *v++;
		}
		items[count][n] = 0;
		if (*v == '"') v = v + 1;
		count = count + 1;
		if (count == max_items) break;
		v = json_skip_ws(v);
		if (*v == ',') { v = v + 1; continue; }
		if (*v == ']') { v = v + 1; break; }
	}
	if (out_count) *out_count = count;
	if (out_pos) *out_pos = (int)(v - src);
	return 1;
}
