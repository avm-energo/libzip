cmake_minimum_required(VERSION 3.10)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
if (${CMAKE_VERSION} VERSION_LESS "3.17.0")
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake-compat)
endif()

project(avm-libzip
  VERSION 1.11.4
  LANGUAGES C)

option(ENABLE_FDOPEN "Enable zip_fdopen, which is not allowed in Microsoft CRT secure libraries" ON)

include(CheckFunctionExists)
include(CheckIncludeFiles)
include(CheckLibraryExists)
include(CheckSymbolExists)
include(CheckTypeSize)
include(CheckCSourceRuns)
include(CheckCSourceCompiles)
include(CheckStructHasMember)
include(TestBigEndian)
include(GNUInstallDirs)

option(BUILD_SHARED_LIBS "Build shared libraries" ON)

if(BUILD_SHARED_LIBS)
  set(HAVE_SHARED TRUE)
else()
  set(ZIP_STATIC TRUE)
endif()

# Checks

# Request ISO C secure library functions (memcpy_s &c)
list(APPEND CMAKE_REQUIRED_DEFINITIONS -D__STDC_WANT_LIB_EXT1__=1)

check_function_exists(_close HAVE__CLOSE)
check_function_exists(_dup HAVE__DUP)
check_function_exists(_fdopen HAVE__FDOPEN)
check_function_exists(_fileno HAVE__FILENO)
check_function_exists(_fseeki64 HAVE__FSEEKI64)
check_function_exists(_fstat64 HAVE__FSTAT64)
check_function_exists(_setmode HAVE__SETMODE)
check_function_exists(_stat64 HAVE__STAT64)
check_symbol_exists(_snprintf stdio.h HAVE__SNPRINTF)
check_symbol_exists(_snprintf_s stdio.h HAVE__SNPRINTF_S)
check_symbol_exists(_snwprintf_s stdio.h HAVE__SNWPRINTF_S)
check_function_exists(_strdup HAVE__STRDUP)
check_symbol_exists(_stricmp string.h HAVE__STRICMP)
check_function_exists(_strtoi64 HAVE__STRTOI64)
check_function_exists(_strtoui64 HAVE__STRTOUI64)
check_function_exists(_unlink HAVE__UNLINK)
check_function_exists(arc4random HAVE_ARC4RANDOM)
check_function_exists(clonefile HAVE_CLONEFILE)
check_function_exists(explicit_bzero HAVE_EXPLICIT_BZERO)
check_function_exists(explicit_memset HAVE_EXPLICIT_MEMSET)
check_function_exists(fchmod HAVE_FCHMOD)
check_function_exists(fileno HAVE_FILENO)
check_function_exists(fseeko HAVE_FSEEKO)
check_function_exists(ftello HAVE_FTELLO)
check_function_exists(getprogname HAVE_GETPROGNAME)
check_function_exists(GetSecurityInfo HAVE_GETSECURITYINFO)
check_symbol_exists(localtime_r time.h HAVE_LOCALTIME_R)
check_symbol_exists(localtime_s time.h HAVE_LOCALTIME_S)
check_function_exists(memcpy_s HAVE_MEMCPY_S)
check_function_exists(random HAVE_RANDOM)
check_function_exists(setmode HAVE_SETMODE)
check_symbol_exists(snprintf stdio.h HAVE_SNPRINTF)
check_symbol_exists(snprintf_s stdio.h HAVE_SNPRINTF_S)
check_symbol_exists(strcasecmp strings.h HAVE_STRCASECMP)
check_function_exists(strdup HAVE_STRDUP)
check_function_exists(strerror_s HAVE_STRERROR_S)
check_function_exists(strerrorlen_s HAVE_STRERRORLEN_S)
check_function_exists(stricmp HAVE_STRICMP)
check_function_exists(strncpy_s HAVE_STRNCPY_S)
check_function_exists(strtoll HAVE_STRTOLL)
check_function_exists(strtoull HAVE_STRTOULL)

check_include_files("sys/types.h;sys/stat.h;fts.h" HAVE_FTS_H)
# fts functions may be in external library
if(HAVE_FTS_H)
  check_function_exists(fts_open HAVE_FTS_OPEN)
  if(NOT HAVE_FTS_OPEN)
    check_library_exists(fts fts_open "" HAVE_LIB_FTS)
  else(NOT HAVE_FTS_OPEN)
    set(HAVE_LIB_FTS "" CACHE INTERNAL "")
  endif(NOT HAVE_FTS_OPEN)
else(HAVE_FTS_H)
  set(HAVE_LIB_FTS "" CACHE INTERNAL "")
endif(HAVE_FTS_H)

if(HAVE_LIB_FTS)
  set(FTS_LIB fts CACHE INTERNAL "")
else()
  set(FTS_LIB "" CACHE INTERNAL "")
endif()

check_include_files(stdbool.h HAVE_STDBOOL_H)
check_include_files(strings.h HAVE_STRINGS_H)
check_include_files(unistd.h Z_HAVE_UNISTD_H)

check_include_files(inttypes.h HAVE_INTTYPES_H_LIBZIP)
check_include_files(stdint.h HAVE_STDINT_H_LIBZIP)
check_include_files(sys/types.h HAVE_SYS_TYPES_H_LIBZIP)

# TODO: fix test
# this test does not find __progname even when it exists
#check_symbol_exists(__progname stdlib.h HAVE___PROGNAME)

check_type_size(__int8 __INT8_LIBZIP)
check_type_size(int8_t INT8_T_LIBZIP)
check_type_size(uint8_t UINT8_T_LIBZIP)
check_type_size(__int16 __INT16_LIBZIP)
check_type_size(int16_t INT16_T_LIBZIP)
check_type_size(uint16_t UINT16_T_LIBZIP)
check_type_size(__int32 __INT32_LIBZIP)
check_type_size(int32_t INT32_T_LIBZIP)
check_type_size(uint32_t UINT32_T_LIBZIP)
check_type_size(__int64 __INT64_LIBZIP)
check_type_size(int64_t INT64_T_LIBZIP)
check_type_size(uint64_t UINT64_T_LIBZIP)
check_type_size("short" SHORT_LIBZIP)
check_type_size("int" INT_LIBZIP)
check_type_size("long" LONG_LIBZIP)
check_type_size("long long" LONG_LONG_LIBZIP)
check_type_size("off_t" SIZEOF_OFF_T)
check_type_size("size_t" SIZEOF_SIZE_T)

check_c_source_compiles("#include <sys/ioctl.h>
#include <linux/fs.h>
int main(int argc, char *argv[]) { unsigned long x = FICLONERANGE; }" HAVE_FICLONERANGE)

test_big_endian(WORDS_BIGENDIAN)

include(zlib)

if(MSVC)
  add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
  add_compile_definitions(_CRT_NONSTDC_NO_DEPRECATE)
endif(MSVC)

# for code completion frameworks
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Targets
include(CheckFunctionExists)

set(CMAKE_C_VISIBILITY_PRESET hidden)

# create zip_err_str.c from zip.h and zipint.h
add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/zip_err_str.c
  COMMAND "${CMAKE_COMMAND}"
    "-DPROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}"
    "-DCMAKE_CURRENT_BINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}"
    "-P" "${PROJECT_SOURCE_DIR}/cmake/GenerateZipErrorStrings.cmake"
  DEPENDS
    ${PROJECT_SOURCE_DIR}/cmake/GenerateZipErrorStrings.cmake
    ${PROJECT_SOURCE_DIR}/zip.h
    ${PROJECT_SOURCE_DIR}/zipint.h
  COMMENT "Generating zip_err_str.c"
)

add_library(${PROJECT_NAME}
    zip_add.c
    zip_add_dir.c
    zip_add_entry.c
    zip_algorithm_deflate.c
    zip_buffer.c
    zip_close.c
    zip_delete.c
    zip_dir_add.c
    zip_dirent.c
    zip_discard.c
    zip_entry.c
    zip_error.c
    zip_error_clear.c
    zip_error_get.c
    zip_error_get_sys_type.c
    zip_error_strerror.c
    zip_error_to_str.c
    zip_extra_field.c
    zip_extra_field_api.c
    zip_fclose.c
    zip_fdopen.c
    zip_file_add.c
    zip_file_error_clear.c
    zip_file_error_get.c
    zip_file_get_comment.c
    zip_file_get_external_attributes.c
    zip_file_get_offset.c
    zip_file_rename.c
    zip_file_replace.c
    zip_file_set_comment.c
    zip_file_set_encryption.c
    zip_file_set_external_attributes.c
    zip_file_set_mtime.c
    zip_file_strerror.c
    zip_fopen.c
    zip_fopen_encrypted.c
    zip_fopen_index.c
    zip_fopen_index_encrypted.c
    zip_fread.c
    zip_fseek.c
    zip_ftell.c
    zip_get_archive_comment.c
    zip_get_archive_flag.c
    zip_get_encryption_implementation.c
    zip_get_file_comment.c
    zip_get_name.c
    zip_get_num_entries.c
    zip_get_num_files.c
    zip_hash.c
    zip_io_util.c
    zip_libzip_version.c
    zip_memdup.c
    zip_name_locate.c
    zip_new.c
    zip_open.c
    zip_pkware.c
    zip_progress.c
    zip_realloc.c
    zip_rename.c
    zip_replace.c
    zip_set_archive_comment.c
    zip_set_archive_flag.c
    zip_set_default_password.c
    zip_set_file_comment.c
    zip_set_file_compression.c
    zip_set_name.c
    zip_source_accept_empty.c
    zip_source_begin_write.c
    zip_source_begin_write_cloning.c
    zip_source_buffer.c
    zip_source_call.c
    zip_source_close.c
    zip_source_commit_write.c
    zip_source_compress.c
    zip_source_crc.c
    zip_source_error.c
    zip_source_file_common.c
    zip_source_file_stdio.c
    zip_source_free.c
    zip_source_function.c
    zip_source_get_dostime.c
    zip_source_get_file_attributes.c
    zip_source_is_deleted.c
    zip_source_layered.c
    zip_source_open.c
    zip_source_pass_to_lower_layer.c
    zip_source_pkware_decode.c
    zip_source_pkware_encode.c
    zip_source_read.c
    zip_source_remove.c
    zip_source_rollback_write.c
    zip_source_seek.c
    zip_source_seek_write.c
    zip_source_stat.c
    zip_source_supports.c
    zip_source_tell.c
    zip_source_tell_write.c
    zip_source_window.c
    zip_source_write.c
    zip_source_zip.c
    zip_source_zip_new.c
    zip_stat.c
    zip_stat_index.c
    zip_stat_init.c
    zip_strerror.c
    zip_string.c
    zip_unchange.c
    zip_unchange_all.c
    zip_unchange_archive.c
    zip_unchange_data.c
    zip_utf-8.c
  ${CMAKE_CURRENT_BINARY_DIR}/zip_err_str.c)

add_library(avm-energo::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

if(WIN32)
  target_compile_definitions(${PROJECT_NAME} PRIVATE WIN32_LEAN_AND_MEAN)
  target_sources(${PROJECT_NAME} PRIVATE
    zip_source_file_win32.c
    zip_source_file_win32_named.c
    zip_source_file_win32_utf16.c
    zip_source_file_win32_utf8.c
    )
  if(CMAKE_SYSTEM_NAME MATCHES WindowsPhone OR CMAKE_SYSTEM_NAME MATCHES WindowsStore)
    target_sources(${PROJECT_NAME} PRIVATE zip_random_uwp.c)
  else()
    target_sources(${PROJECT_NAME} PRIVATE zip_source_file_win32_ansi.c zip_random_win32.c)
    target_link_libraries(${PROJECT_NAME} PRIVATE advapi32)
  endif()
else(WIN32)
  target_sources(${PROJECT_NAME} PRIVATE
    zip_source_file_stdio_named.c
    zip_random_unix.c
    )
endif(WIN32)

target_link_libraries(${PROJECT_NAME} PUBLIC avm-zlib)

target_include_directories(${PROJECT_NAME}
  PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}>
  $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )

# fixed size integral types

if(HAVE_INTTYPES_H_LIBZIP)
  set(LIBZIP_TYPES_INCLUDE "#if !defined(__STDC_FORMAT_MACROS)
#define __STDC_FORMAT_MACROS 1
#endif
#include <inttypes.h>")
elseif(HAVE_STDINT_H_LIBZIP)
  set(LIBZIP_TYPES_INCLUDE "#include <stdint.h>")
elseif(HAVE_SYS_TYPES_H_LIBZIP)
  set(LIBZIP_TYPES_INCLUDE "#include <sys/types.h>")
endif()

if(HAVE_INT8_T_LIBZIP)
  set(ZIP_INT8_T int8_t)
elseif(HAVE___INT8_LIBZIP)
  set(ZIP_INT8_T __int8)
else()
  set(ZIP_INT8_T "signed char")
endif()

if(HAVE_UINT8_T_LIBZIP)
  set(ZIP_UINT8_T uint8_t)
elseif(HAVE___INT8_LIBZIP)
  set(ZIP_UINT8_T "unsigned __int8")
else()
  set(ZIP_UINT8_T "unsigned char")
endif()

if(HAVE_INT16_T_LIBZIP)
  set(ZIP_INT16_T int16_t)
elseif(HAVE___INT16_LIBZIP)
  set(INT16_T_LIBZIP __int16)
elseif(SHORT_LIBZIP EQUAL 2)
  set(INT16_T_LIBZIP short)
endif()

if(HAVE_UINT16_T_LIBZIP)
  set(ZIP_UINT16_T uint16_t)
elseif(HAVE___INT16_LIBZIP)
  set(UINT16_T_LIBZIP "unsigned __int16")
elseif(SHORT_LIBZIP EQUAL 2)
  set(UINT16_T_LIBZIP "unsigned short")
endif()

if(HAVE_INT32_T_LIBZIP)
  set(ZIP_INT32_T int32_t)
elseif(HAVE___INT32_LIBZIP)
  set(ZIP_INT32_T __int32)
elseif(INT_LIBZIP EQUAL 4)
  set(ZIP_INT32_T int)
elseif(LONG_LIBZIP EQUAL 4)
  set(ZIP_INT32_T long)
endif()

if(HAVE_UINT32_T_LIBZIP)
  set(ZIP_UINT32_T uint32_t)
elseif(HAVE___INT32_LIBZIP)
  set(ZIP_UINT32_T "unsigned __int32")
elseif(INT_LIBZIP EQUAL 4)
  set(ZIP_UINT32_T "unsigned int")
elseif(LONG_LIBZIP EQUAL 4)
  set(ZIP_UINT32_T "unsigned long")
endif()

if(HAVE_INT64_T_LIBZIP)
  set(ZIP_INT64_T int64_t)
elseif(HAVE___INT64_LIBZIP)
  set(ZIP_INT64_T __int64)
elseif(LONG_LIBZIP EQUAL 8)
  set(ZIP_INT64_T long)
elseif(LONG_LONG_LIBZIP EQUAL 8)
  set(ZIP_INT64_T "long long")
endif()

if(HAVE_UINT64_T_LIBZIP)
  set(ZIP_UINT64_T uint64_t)
elseif(HAVE___INT64_LIBZIP)
  set(ZIP_UINT64_T "unsigned __int64")
elseif(LONG_LIBZIP EQUAL 8)
  set(ZIP_UINT64_T "unsigned long")
elseif(LONG_LONG_LIBZIP EQUAL 8)
  set(ZIP_UINT64_T "unsigned long long")
endif()

# write out config file
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in ${PROJECT_BINARY_DIR}/config.h)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/zipconf.h.in ${PROJECT_BINARY_DIR}/zipconf.h)

install(TARGETS ${PROJECT_NAME}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}-targets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(FILES zip.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# create package config file
include(CMakePackageConfigHelpers)
write_basic_package_version_file("${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
  COMPATIBILITY AnyNewerVersion)

configure_package_config_file("${PROJECT_NAME}-config.cmake.in" "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake"
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})

# installation
install(FILES ${PROJECT_BINARY_DIR}/zipconf.h DESTINATION include)
install(FILES ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  )
install(EXPORT ${PROJECT_NAME}-targets NAMESPACE ${PROJECT_NAME}:: FILE ${PROJECT_NAME}-targets.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  )

set(VERSION_IN ${CMAKE_CURRENT_SOURCE_DIR}/VERSION.in)
set(VERSION_OUT ${CMAKE_CURRENT_SOURCE_DIR}/package/src/VERSION)
configure_file(${VERSION_IN} ${VERSION_OUT} @ONLY)
