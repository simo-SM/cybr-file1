/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ui.h                                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:36 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:36 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef UI_H
# define UI_H

void	ui_clear(void);
void	ui_print_hr(void);
void	ui_pause(void);
void	ui_read_line(char *buf, int size);
int		ui_prompt_yes_no(const char *prompt);
int		ui_menu(const char *title, const char **items, int count);

#endif
