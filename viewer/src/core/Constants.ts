export const DOMName = {
  renderTarget: '#uiroot',
} as const;


const baseUrl = location.origin;
const apiUrl = baseUrl + '/api';
export const APIURL = {
  logon: `${apiUrl}/logon`,
  register: `${apiUrl}/register`,
};
