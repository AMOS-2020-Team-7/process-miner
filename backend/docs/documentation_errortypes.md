# Process Miner Logs Error Documentation

## Identified Errors

8 different error types were identified in the logs:

1. `error_401_psu_credentials_invalid`

2. `error_ASPSP_not_found`
3. `error_400_service_invalid_for_step_create_consent`
4. `error_403_consent_invalid`
5. `error_internal_server`
6. `error_service_unavailable`
7. `error_400_format`
8. `error_sca_status_405`

The corresponding graphs to visualize the flow of an error can be generated and saved as a heuristic net (.svg) by choosing one of the eight error types.

Naming condition: `heuristicnet_{errortype}.svg`

The error type can be changed within process_miner `__main__.py`.
