var LinkRow = React.createClass({
    render: function () {
        if (this.props.link.failed) {
            return (
            <li className="collection-item">
                {this.props.link.title}
                <div className="secondary-content"><a onClick={this.props.deleteLink} href="#!"><i className="small mdi-action-delete"></i></a>
                <a href={this.props.link.edit_url}><i className="small mdi-editor-mode-edit"></i></a>
                </div>
                <span className="red-txt secondary-content">[Failed!]</span>
            </li>
            )
        } else {
            if (this.props.link.published) {
            return (
            <li className="collection-item">
                {this.props.link.title}
                <div className="secondary-content"><a onClick={this.props.deleteLink} href="#!"><i className="small mdi-action-delete"></i></a>
                <a href={this.props.link.edit_url}><i className="small mdi-editor-mode-edit"></i></a>
                </div>
            </li>
            )
        } else {
            return (
                <li className="collection-item">
                    {this.props.link.title}
                <div className="secondary-content">Processing...
                </div>
                </li>
            )
            };
        };
    }
});

var LinksTable = React.createClass({
    deleteLink: function (podcastItem) {
        var that = this;
        this.state.data.splice(this.state.data.indexOf(podcastItem), 1);
        this.setState({date: this.state.data});
        $.ajax({
            url: podcastItem.delete_url,
            method: 'DELETE',
            dataType: 'json',
            success: function (data) {
                that.loadResponsesFromServer();
            },
            error: function (xhr, status, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    },
    loadResponsesFromServer: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function () {
        this.loadResponsesFromServer();
        setInterval(this.loadResponsesFromServer, this.props.pollInterval);
        $('#feed').collapsible();
    },
    render: function () {
        var that = this;
        var linkNodes = this.state.data.map(function (link, index) {
                return (
                    <LinkRow link={link} deleteLink={that.deleteLink.bind(null, link)} key={index}>
                    </LinkRow>
                    )
        });
        return (
            <ul className="collection">
            {linkNodes}
            </ul>
        );
    }
});
