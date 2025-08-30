import React from "react";
import type Application from "~/core/Application";

type Props = { app: Application; };
type State = {};

export default class UserInterface extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props);
    this.state = {};
  }

  override componentDidMount(): void {
    this.props.app.components.ui = this;
  }

  override componentWillUnmount(): void {
    this.props.app.components.ui = undefined;
  }

  override render() {
    return (
      <div id="ui"></div>
    );
  }

}
