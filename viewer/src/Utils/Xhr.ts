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
    });

    return response;
  }

  static auth(
    id: string,
    pass: string
  ) {
    return `Basic ${btoa(`${id}:${pass}`)}`;
  }

}
