export const environment = {
  production: true,
  // this will be filled with actual values during docker build
  // see scripts/set_backend_access_data.sh and Dockerfile
  backendHost: '###BACKEND_HOST###',
  backendPort: '###BACKEND_PORT###'
};
