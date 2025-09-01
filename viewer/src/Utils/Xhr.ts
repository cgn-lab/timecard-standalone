export default class Xhr {

  static async get(
    url: string,
    auth?: string,
  ) {

    // ヘッダ作成
    const header: HeadersInit = {
      Accept: 'application/json',
    };
    if (auth) {
      header.Authorization = auth;
    }

    // 送信
    const response = await fetch(url, {
      method: 'GET',
      headers: header,
      credentials: 'same-origin',
    });

    return response;
  }

  static async post(
    url: string,
    body?: any,
    auth?: string,
  ) {

    // ヘッダ作成
    const header: HeadersInit = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };
    if (auth) {
      header.Authorization = auth;
    }

    // 送信
    const response = await fetch(url, {
      method: 'POST',
      headers: header,
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'same-origin',
    });

    return response;
  }

  static auth(
    id: string,
    pass: string,
  ) {
    return `Basic ${btoa(`${id}:${pass}`)}`;
  }

}
