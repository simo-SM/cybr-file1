/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tests.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:31 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:31 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "signature.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

static char	*capture_output(const char *fname)
{
	FILE	*r;
	long	sz;
	char	*buf;
	size_t	rd;

	(void)freopen(fname, "w", stdout);
	ft_print_comb();
	fflush(stdout);
	(void)freopen("CON", "w", stdout);
	r = fopen(fname, "rb");
	if (!r)
		return (NULL);
	fseek(r, 0, 2);
	sz = ftell(r);
	fseek(r, 0, 0);
	buf = (char *)malloc((size_t)sz + 1);
	rd = fread(buf, 1, (size_t)sz, r);
	fclose(r);
	buf[rd] = 0;
	remove(fname);
	return (buf);
}

int	main(void)
{
	char	*s;
	char	*exp;
	int		passed;
	int		total;

	s = capture_output("comb.txt");
	passed = 0;
	total = 1;
	exp = "012, 013, 014, 015, 016, 017, 018, 019, 023, 024, 025, "
		"026, 027, 028, 029, 034, 035, 036, 037, 038, 039, 045, "
		"046, 047, 048, 049, 056, 057, 058, 059, 067, 068, 069, "
		"078, 079, 089, 123, 124, 125, 126, 127, 128, 129, 134, "
		"135, 136, 137, 138, 139, 145, 146, 147, 148, 149, 156, "
		"157, 158, 159, 167, 168, 169, 178, 179, 189, 234, 235, "
		"236, 237, 238, 239, 245, 246, 247, 248, 249, 256, 257, "
		"258, 259, 267, 268, 269, 278, 279, 289, 345, 346, 347, "
		"348, 349, 356, 357, 358, 359, 367, 368, 369, 378, 379, "
		"389, 456, 457, 458, 459, 467, 468, 469, 478, 479, 489, "
		"567, 568, 569, 578, 579, 589, 678, 679, 689, 789\n";
	if (s && strcmp(s, exp) == 0)
		passed = 1;
	if (s)
		free(s);
	printf("RESULT: %d/%d\n", passed, total);
	return (0);
}
