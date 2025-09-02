/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   json.h                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/02 04:22:35 by student          #+#    #+#             */
/*   Updated: 2025/09/02 04:22:35 by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef JSON_H
# define JSON_H

/*
** Minimal JSON helpers used by CLG MVP.
** These are simple, not general-purpose.
** They are enough for the provided content.
*/

char	*json_skip_ws(const char *p);
int		json_extract_string(const char *src, const char *key,
			int start_pos, char *out);
int		json_extract_int(const char *src, const char *key, int start_pos,
			int *out_value);
int		json_extract_string_array(const char *src, const char *key,
			int start_pos, char items[][256]);

#endif
