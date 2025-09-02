/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ui.c                                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:36 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:36 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ui.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

void ui_clear(void) {
	system("cls");
}

void ui_print_hr(void) {
	printf("============================================\n");
}

void ui_pause(void) {
	printf("Press Enter to continue...");
	fflush(stdout);
	char tmp[8];
	if (!fgets(tmp, sizeof(tmp), stdin)) {
		/* ignore */
	}
}

void ui_read_line(char* buf, int size) {
	if (!fgets(buf, size, stdin)) {
		buf[0] = 0;
		return;
	}
	int n = (int)strlen(buf);
	while (n != 0) {
		char c = buf[n - 1];
		if (c == '\n' || c == '\r') {
			buf[n - 1] = 0;
			n = n - 1;
		} else {
			break;
		}
	}
}

int ui_prompt_yes_no(const char* prompt) {
	char line[16];
	for (;;) {
		printf("%s [y-n]: ", prompt);
		ui_read_line(line, sizeof(line));
		if (line[0] == 'y' || line[0] == 'Y') return 1;
		if (line[0] == 'n' || line[0] == 'N') return 0;
		printf("Please type y or n.\n");
	}
}

int ui_menu(const char* title, const char** items, int count) {
	for (;;) {
		ui_clear();
		printf("%s\n", title);
		ui_print_hr();
		int i = 0;
		while (i != count) {
			printf("  %d) %s\n", i + 1, items[i]);
			i = i + 1;
		}
		ui_print_hr();
		printf("Choose 1..%d: ", count);
		char line[32];
		ui_read_line(line, sizeof(line));
		int chosen_index = -1;
		i = 0;
		while (i != count) {
			char num[16];
			sprintf(num, "%d", i + 1);
			if (strcmp(line, num) == 0) {
				chosen_index = i;
				break;
			}
			i = i + 1;
		}
		if (chosen_index != -1) {
			return chosen_index;
		}
		printf("Invalid choice.\n");
		ui_pause();
	}
}
