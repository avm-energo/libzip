include(FetchContent)

FetchContent_Declare(avm-zlib
  GIT_REPOSITORY    https://github.com/avm-energo/zlib.git
  GIT_TAG           v2.0.0
)

FetchContent_MakeAvailable(avm-zlib)
