/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   fs.h                                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:32 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:32 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FS_H
# define FS_H

# ifndef CLG_PATH_MAX
#  define CLG_PATH_MAX 1024
# endif

int		fs_file_exists(const char *path);
int		fs_dir_exists(const char *path);
int		fs_ensure_dir(const char *path);
void	fs_path_join(const char *a, const char *b, char *out, int out_size);
char	*fs_read_all_text(const char *path);
int		fs_write_all_text(const char *path, const char *text);
void	fs_get_exe_dir(char *out, int out_size);
void	fs_normalize_slashes(char *p);

#endif
