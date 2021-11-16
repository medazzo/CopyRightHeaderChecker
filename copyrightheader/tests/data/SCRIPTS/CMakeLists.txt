# Easin Comm tests Binary'

INCLUDE_DIRECTORIES("${CMAKE_CURRENT_SOURCE_DIR}/../src/")

add_executable(testfullecomm EasinCommTestDuplex.cpp)
target_link_libraries( testfullecomm ecomm)
install(TARGETS testfullecomm DESTINATION bin)
target_link_libraries(testfullecomm -lpthread)


add_executable(testecomm     EasinCommTest.cpp)
target_link_libraries( testecomm ecomm)
install(TARGETS testecomm DESTINATION bin)
target_link_libraries(testecomm -lpthread)
