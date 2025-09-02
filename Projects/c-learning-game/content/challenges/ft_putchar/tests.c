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

static void	capture_begin(FILE **old)
{
	FILE	*f;

	*old = stdout;
	f = freopen("ft_putchar_out.txt", "w", stdout);
	(void)f;
}

static char	*capture_end(void)
{
	FILE	*f;
	FILE	*r;
	long	sz;
	char	*buf;
	size_t	rd;

	fflush(stdout);
	f = freopen("CON", "w", stdout);
	(void)f;
	r = fopen("ft_putchar_out.txt", "rb");
	if (!r)
		return (NULL);
	fseek(r, 0, 2);
	sz = ftell(r);
	fseek(r, 0, 0);
	buf = (char *)malloc((size_t)sz + 1);
	rd = fread(buf, 1, (size_t)sz, r);
	fclose(r);
	buf[rd] = 0;
	remove("ft_putchar_out.txt");
	return (buf);
}

static int	test_putchar_one(void)
{
	FILE	*old;
	char	*s;
	int		ok;

	old = NULL;
	capture_begin(&old);
	ft_putchar('A');
	s = capture_end();
	ok = 0;
	if (s && strcmp(s, "A") == 0)
		ok = 1;
	free(s);
	return (ok);
}

int	main(void)
{
	int	passed;
	int	total;

	passed = 0;
	total = 0;
	total = total + 1;
	if (test_putchar_one())
		passed = passed + 1;
	printf("RESULT: %d/%d\n", passed, total);
	return (0);
}
