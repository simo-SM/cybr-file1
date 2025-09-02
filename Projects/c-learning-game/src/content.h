/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   content.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:32 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:32 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#pragma once
#include "game.h"

void	content_show_topics(const char *content_dir);
void	content_run_quiz(const char *content_dir, GameState *state);
void	content_challenges_menu(const char *content_dir,
			GameState *state, const char *gcc_path);
