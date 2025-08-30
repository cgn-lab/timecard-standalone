import React from "react";
import ReactDOM from "react-dom/client";
import { APIURL, DOMName } from "~/core/Constants";
import UserInterface from "~/components/UserInterface";
import Xhr from "~/Utils/Xhr";

export default class Application {
  components: Components;

  constructor() {
    this.components = {};

    // TODO:
    // render() は _init() と別で走らせて 処理後に再描画のほうがUXよさそう
    this._init().then(() => {
      this.render();
    });
  }

  private async _init() {

    // Basic認証
    let response = await Xhr.get(APIURL.logon, Xhr.auth('user', 'pass'));
    if (response.ok) {
      const content = await response.json();
      console.log(content);
    }

    // Bearer認証
    response = await Xhr.get(APIURL.logon, 'Bearer tokentokentoken');
    if (response.ok) {
      const content = await response.json();
      console.log(content);
    }

    // 認証なし
    response = await Xhr.get(APIURL.logon);
    if (response.ok) {
      const content = await response.json();
      console.log(content);
    }
    return;

  }

  render() {
    if (this.components.ui) {

      // 再描画
      this.components.ui.forceUpdate();

    } else {

      // 描画対象を取得
      const renderTargetName = DOMName.renderTarget;
      const renderTarget = document.querySelector(renderTargetName);
      if (!renderTarget) {
        throw new Error(`描画対象が見つかりません: ${renderTargetName}`);
      }

      // 描画
      const root = ReactDOM.createRoot(renderTarget);
      const jsxElement = React.createElement(UserInterface, { app: this });
      root.render(jsxElement);
    }
  }

}

type Components = {
  ui?: UserInterface,
};
