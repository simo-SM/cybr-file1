/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   game.h                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:34 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:34 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GAME_H
# define GAME_H

# define CLG_PATH_MAX 1024

typedef struct s_gamestate
{
	char	base_dir[CLG_PATH_MAX];
	char	content_dir[CLG_PATH_MAX];
	char	workspace_dir[CLG_PATH_MAX];
	char	save_dir[CLG_PATH_MAX];
	int		best_score_c_basics;
	char	status_putchar[16];
	char	status_isneg[16];
	char	status_comb[16];
}			t_gamestate;

void	game_init(t_gamestate *g);
void	game_load(t_gamestate *g);
void	game_save(const t_gamestate *g);
void	game_main(t_gamestate *g, const char *gcc_path);

#endif
