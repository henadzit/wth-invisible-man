cmake_minimum_required(VERSION 2.8)
project( InvisibleMan )
find_package(CUDA REQUIRED)
find_package( OpenCV REQUIRED )

add_definitions(-DHAVE_ALLOCA -DHAVE_ALLOCA_H -DHAVE_LIBPTHREAD -DHAVE_UNISTD_H)
SET(CUDA_HOST_COMPILER "/usr/bin/clang")
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} -L/usr/local/cuda/lib -lcuda -lcudart" )

include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( InvisibleMan main.cpp )
target_link_libraries( InvisibleMan ${OpenCV_LIBS} ${CUDA_LIBS} )
