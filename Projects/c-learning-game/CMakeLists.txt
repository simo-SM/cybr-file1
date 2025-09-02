cmake_minimum_required(VERSION 3.15)

project(CLG C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Global compile options
add_compile_options(-std=c99 -O2 -Wall -Wextra -Werror)

# Sources
set(CLG_SOURCES
  src/main.c
  src/ui.c
  src/game.c
  src/content.c
  src/grader.c
  src/fs.c
  src/json.c
)

add_executable(clg ${CLG_SOURCES})

target_include_directories(clg PRIVATE
  ${CMAKE_SOURCE_DIR}/src
  ${CMAKE_SOURCE_DIR}/vendor/cjson
)

