/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:36 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:36 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "game.h"
#include "ui.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

int	main(void)
{
	GameState	g;
	const char	*gcc_path;

	game_init(&g);
	game_load(&g);
	gcc_path = getenv("CC");
	if (!gcc_path || strlen(gcc_path) == 0)
		gcc_path = "gcc";
	game_main(&g, gcc_path);
	return (0);
}
