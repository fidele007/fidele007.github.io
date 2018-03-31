if (typeof document.onselectstart != "undefined") {
    document.onselectstart = new Function("return false");
} else {
    document.onmousedown = new Function("return false");
    document.onmouseup = new Function("return true");
}

$(document).ready(function () {
    function iOSversion() {
        if (/iP(hone|od|ad)/.test(navigator.platform)) {
            // supports iOS 2.0 and later: <http://bit.ly/TJjs1V>
            var v = (navigator.appVersion).match(/OS (\d+)_(\d+)_?(\d+)?/);
            return [parseInt(v[1], 10), parseInt(v[2], 10), parseInt(v[3] || 0, 10)];
        }
    }

    $(".version-check").html("Your iOS Version: " + iOSversion());

    var dPackage = getParameterByName("p");
    if (!dPackage) {
        $(".package-error").text("This package doesn't seem to exist :(").css("display", "block");
        $(".package-info").css("display", "none");
        $(".package-name").text("Not Found");
        return;
    }

    $.getJSON("packages/" + dPackage + ".json", function (data) {
            document.title = data.name + " by " + data.author;
            $(".package-name").text(data.name);
            $(".package-desc").html(data.description);
            $(".latest-version").text(data.version);
            $(".package-author").text(" by " + data.author);

            var cList = $(".changelog-list");
            var changes = data.changelog[data.version];
            for (var i = 0; i < changes.length - 1; i++) {
                cList.append("<div style=\"border-bottom:1px solid #dad8d8;margin-left:-10px;margin-right:-10px;padding-bottom:7px;margin-bottom:7px;\">" + "<div style=\"margin-left:15px;margin-right:15px\">" + changes[i] + "</div>" + "</div>")
            }
            cList.append("<div style=\"margin-left:5px;margin-right:5px\">" + changes[changes.length - 1] + "</div>");
            $(".screenshots-header").click(function () {
                $(".panel-default>.screenshots-header").toggleClass('toggle');
                $(".screenshots").slideToggle(function () {});
            });
            var count = 0;
            var screenshots = data.screenshots;
            var sKeys = Object.keys(screenshots);
            if (jQuery.isEmptyObject(screenshots)) {
                $("#screenshot-tab").hide();
            } else {
                for (var s in sKeys) {
                    var screenshot = sKeys[s];
                    if (count % 2 === 0) {
                        $(".screenshots").append("<div class=\"subshots\"></div>");
                    }
                    $(".screenshots .subshots:last-child").append("<div class=\"col-xs-12\"><img class=\"img-responsive\" src=\"screenshots/" + dPackage + "/" + screenshot + "\" title=\"" + screenshots[screenshot] + "\"><p><strong>" + screenshots[screenshot] + "</strong></p><br></div>");
                    count += 1;
                }
            }

            $(".fullchangelog-header").click(function () {
                $(".panel-default>.fullchangelog-header").toggleClass('toggle');
                $(".fullchangelog").slideToggle(function () {});
            });
            var latest = data.version;
            var versions = Object.keys(data.changelog).reverse();
            for (var v in versions) {
                var version = versions[v];
                var panel = $("<div class=\"panel-default \"></div>");
                panel.append(" <div class=\"panel-heading\" style=\"text-transform: uppercase; font-size:15px; font-weight:400; color: #6d6d72;\">" + version + "</div>");
                panel.append(" <div class=\"panel-body changelog-list\" style=\"padding:10px;\"></div>");
                if (version === latest) {
                    panel.find(".panel-heading").append(" <div class=\"label label-info badge-label latest-version\">Current</div>");
                }
                var changes = data.changelog[version];
                for (var i = 0; i < changes.length - 1; i++) {
                    var change = changes[i];
                    panel.find(".changelog-list").append("<div style=\"border-bottom:1px solid #dad8d8;margin-left:-10px;margin-right:-10px;padding-bottom:7px;margin-bottom:7px;\">" + "<div style=\"margin-left:15px;margin-right:15px\">" + change + "</div>" + "</div>");
                }
                panel.find(".changelog-list").append("<div style=\"margin-left:5px;margin-right:5px\">" + changes[changes.length - 1] + "</div>");
                $(".package-versions").append(panel);
            }

            var links = data.links;
            var extra = {
                "<img class=\"icon\" src=\"info.png\"><span>Twitter @kienforcefidele</span>": "https://twitter.com/fidel3007",
                "<img class=\"icon\" src=\"love.png\"><span>Give Energy ༼ つ ◕_◕ ༽つ <span style=\"font-style:italic;font-weight:bold;\"><span style=\"color:#253b80;\">Pay</span><span style=\"color:#419bd7;\">Pal</strong></span></span>": "https://paypal.me/fidele007"
            };
            $.extend(links, extra);
            var lKeys = Object.keys(links);
            for (var l in lKeys) {
                var link = lKeys[l];
                var wrap = $("<a style=\"color:#333;\" href=\"" + links[link] + "\" target=\"_blank\"><li class=\"list-group-item\"></li></a>");
                wrap.find(".list-group-item").append($.parseHTML(link));
                $(".package-buttons .list-group").append(wrap);
            }
        })

        .fail(function () {
            $(".package-error").text("An error occurred while retrieving package info!").css("display", "block");
            $(".package-info").css("display", "none");
            $(".package-name").text("Repository Error");
            return;
        });

    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
});