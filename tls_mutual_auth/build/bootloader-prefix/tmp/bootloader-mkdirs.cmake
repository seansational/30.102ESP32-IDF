# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Espressif/frameworks/esp-idf-v5.1.2/components/bootloader/subproject"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/tmp"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/src"
  "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/user/Desktop/GIT/30.102ESP32-IDF/aws/esp-aws-iot/examples/mqtt/tls_mutual_auth/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
