/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   grader.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:35 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:35 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GRADER_H
# define GRADER_H

int	grader_prepare_user_code(const char *base_dir,
		const char *workspace_dir, const char *id);
int	grader_grade(const char *base_dir, const char *workspace_dir,
		const char *id, int *out_passed);
int	grader_grade_full(int *out_total, char *out_log, int log_size,
		const char *gcc_path);

#endif
