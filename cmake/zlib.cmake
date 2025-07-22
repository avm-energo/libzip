include(FetchContent)

FetchContent_Declare(avm-zlib
  GIT_REPOSITORY    https://git.avmenergo.ru/avm-energo/zlib.git
  GIT_TAG           v1.4.1
)

FetchContent_MakeAvailable(avm-zlib)
