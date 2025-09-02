/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tests.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:30 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:30 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "signature.h"
#include "stdio.h"
#include "stdlib.h"

static void	cap_begin(const char *fname)
{
	(void)freopen(fname, "w", stdout);
}

static char	*cap_end(const char *fname)
{
	FILE	*r;
	long	sz;
	char	*buf;
	size_t	rd;

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

static int	is_negative_test(void)
{
	char	*s;
	int		result;

	result = 1;
	cap_begin("neg.txt");
	ft_is_negative(-5);
	s = cap_end("neg.txt");
	if (!s || strcmp(s, "N\n") != 0)
		result = 0;
	free(s);
	cap_begin("zero.txt");
	ft_is_negative(0);
	s = cap_end("zero.txt");
	if (!s || strcmp(s, "P\n") != 0)
		result = 0;
	free(s);
	cap_begin("pos.txt");
	ft_is_negative(7);
	s = cap_end("pos.txt");
	if (!s || strcmp(s, "P\n") != 0)
		result = 0;
	free(s);
	return (result);
}

int	main(void)
{
	int	passed;
	int	total;

	passed = 0;
	total = 0;
	total = total + 1;
	if (is_negative_test())
		passed = passed + 1;
	printf("RESULT: %d/%d\n", passed, total);
	return (0);
}
