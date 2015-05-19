var LinkRow = React.createClass({displayName: "LinkRow",
    render: function () {
        if (this.props.link.failed) {
            return (
            React.createElement("li", {className: "collection-item"}, 
                this.props.link.title, 
                React.createElement("div", {className: "secondary-content"}, React.createElement("a", {onClick: this.props.deleteLink, href: "#!"}, React.createElement("i", {className: "small mdi-action-delete"})), 
                React.createElement("a", {href: this.props.link.edit_url}, React.createElement("i", {className: "small mdi-editor-mode-edit"}))
                ), 
                React.createElement("span", {className: "red-txt secondary-content"}, "[Failed!]")
            )
            )
        } else {
            if (this.props.link.published) {
            return (
            React.createElement("li", {className: "collection-item"}, 
                this.props.link.title, 
                React.createElement("div", {className: "secondary-content"}, React.createElement("a", {onClick: this.props.deleteLink, href: "#!"}, React.createElement("i", {className: "small mdi-action-delete"})), 
                React.createElement("a", {href: this.props.link.edit_url}, React.createElement("i", {className: "small mdi-editor-mode-edit"}))
                )
            )
            )
        } else {
            return (
                React.createElement("li", {className: "collection-item"}, 
                    this.props.link.title, 
                React.createElement("div", {className: "secondary-content"}, "Processing..."
                )
                )
            )
            };
        };
    }
});

var LinksTable = React.createClass({displayName: "LinksTable",
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
                    React.createElement(LinkRow, {link: link, deleteLink: that.deleteLink.bind(null, link), key: index}
                    )
                    )
        });
        return (
            React.createElement("ul", {className: "collection"}, 
            linkNodes
            )
        );
    }
});
