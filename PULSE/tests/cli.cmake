execute_process(COMMAND "${PULSE}" bench --repeat 2 --tasks 3 --words 4 --workers 2
    RESULT_VARIABLE status OUTPUT_VARIABLE output)
string(REGEX MATCHALL "\n" lines "${output}")
list(LENGTH lines count)
if(NOT status EQUAL 0 OR NOT count EQUAL 2 OR
    NOT output MATCHES [[^\{"schema":1,"sample":1,"tasks":3,.*"sample":2,"tasks":3,]])
    message(FATAL_ERROR "Benchmark inesperado: ${status} ${output}")
endif()

foreach(option IN ITEMS --tasks --words --workers --seed --budget-bytes --target-ms)
    execute_process(COMMAND "${PULSE}" run "${option}" -1
        RESULT_VARIABLE status OUTPUT_QUIET ERROR_QUIET)
    if(NOT status EQUAL 2)
        message(FATAL_ERROR "Opcao negativa aceita: ${option}")
    endif()
endforeach()

execute_process(COMMAND "${PULSE}" run --words 4 --budget-bytes 31
    RESULT_VARIABLE status OUTPUT_VARIABLE output ERROR_QUIET)
if(NOT status EQUAL 1 OR NOT output STREQUAL "")
    message(FATAL_ERROR "Orcamento insuficiente deveria falhar sem JSON")
endif()
