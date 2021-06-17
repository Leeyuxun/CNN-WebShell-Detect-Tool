(function (c) {
    var b = {};

    function a(e) {
        if (b[e]) {
            return b[e].exports
        }
        var d = b[e] = {i: e, l: false, exports: {}};
        c[e].call(d.exports, d, d.exports, a);
        d.l = true;
        return d.exports
    }

    a.m = c;
    a.c = b;
    a.d = function (d, f, e) {
        if (!a.o(d, f)) {
            Object.defineProperty(d, f, {enumerable: true, get: e})
        }
    };
    a.r = function (d) {
        if (typeof Symbol !== "undefined" && Symbol.toStringTag) {
            Object.defineProperty(d, Symbol.toStringTag, {value: "Module"})
        }
        Object.defineProperty(d, "__esModule", {value: true})
    };
    a.t = function (g, e) {
        if (e & 1) {
            g = a(g)
        }
        if (e & 8) {
            return g
        }
        if ((e & 4) && typeof g === "object" && g && g.__esModule) {
            return g
        }
        var f = Object.create(null);
        a.r(f);
        Object.defineProperty(f, "default", {enumerable: true, value: g});
        if (e & 2 && typeof g != "string") {
            for (var d in g) {
                a.d(f, d, function (h) {
                    return g[h]
                }.bind(null, d))
            }
        }
        return f
    };
    a.n = function (g) {
        var f = g && g.__esModule ? function d() {
            return g["default"]
        } : function e() {
            return g
        };
        a.d(f, "a", f);
        return f
    };
    a.o = function (d, e) {
        return Object.prototype.hasOwnProperty.call(d, e)
    };
    a.p = "/";
    return a(a.s = 0)
})({
    "./public/assets/sass/app.scss":
    /**************************************!*\
     !*** ./public/assets/sass/app.scss ***!
     \*************************************/
    /* no static exports found */
        (function (b, a) {
        }), "./resources/js/app.js":
    /******************************!*\
     !*** ./resources/js/app.js ***!
     \*****************************/
    /* no static exports found */
        (function (c, b, a) {
            (function (d) {
                var l = d(window), e = d("body");
                feather.replace({"stroke-width": 1.5});
                d(document).on("click", '[data-toggle="fullscreen"]', function () {
                    d(this).toggleClass("active-fullscreen");
                    if (document.fullscreenEnabled) {
                        if (d(this).hasClass("active-fullscreen")) {
                            document.documentElement.requestFullscreen()
                        } else {
                            document.exitFullscreen()
                        }
                    } else {
                        alert("Your browser does not support fullscreen.")
                    }
                    return false
                });
                d(document).on("click", ".overlay", function () {
                    d.removeOverlay();
                    if (e.hasClass("horizontal-navigation")) {
                        d(".horizontal-navigation").removeClass("open")
                    } else {
                        d(".navigation").removeClass("open")
                    }
                    e.removeClass("navigation-show")
                });
                d(document).on("click", "[data-sidebar-target]", function () {
                    var m = d(this).data("sidebar-target");
                    d("body").addClass("no-scroll");
                    d(".sidebar-group").addClass("show");
                    d(".sidebar-group .sidebar").removeClass("show");
                    d(".sidebar-group .sidebar" + m).addClass("show");
                    return false
                });
                d(document).on("click", ".sidebar-group", function (m) {
                    if (d(m.target).is(d(".sidebar-group"))) {
                        d(".sidebar-group").removeClass("show");
                        d("body").removeClass("no-scroll");
                        d(".sidebar-group .sidebar").removeClass("show")
                    }
                });
                d(".navigation .navigation-menu-body .navigation-menu-group ul li a.active").closest("ul").parent("li").addClass("open").closest("ul").parent("li").addClass("open");
                d(".navigation .navigation-menu-body .navigation-menu-group ul li a.active").closest("div").addClass("open");
                d('.navigation .navigation-menu-tab [data-nav-target="#' + d(".navigation .navigation-menu-body .navigation-menu-group ul li a.active").closest("div").attr("id") + '"]').addClass("active");
                d("body.horizontal-navigation .horizontal-navigation ul li a.active").closest("ul").parent("li").addClass("open").closest("ul").parent("li").addClass("open");
                d.createOverlay = function () {
                    if (d(".overlay").length < 1) {
                        e.addClass("no-scroll").append('<div class="overlay"></div>');
                        d(".overlay").addClass("show")
                    }
                };
                d.removeOverlay = function () {
                    e.removeClass("no-scroll");
                    d(".overlay").remove()
                };
                d("[data-backround-image]").each(function (m) {
                    d(this).css("background", "url(" + d(this).data("backround-image") + ")")
                });
                l.on("load", function () {
                    d(".preloader").fadeOut(400, function () {
                    })
                });
                l.on("load", function () {
                    setTimeout(function () {
                        d(".navigation .navigation-menu-body ul li a").each(function () {
                            var m = d(this);
                            if (m.next("ul").length) {
                                m.append('<i class="sub-menu-arrow ti-angle-right"></i>')
                            }
                        });
                        d(".navigation .navigation-menu-body ul li.open>a>.sub-menu-arrow").removeClass("ti-plus").addClass("ti-minus").addClass("fa-rotate-90");
                        d("body.horizontal-navigation .horizontal-navigation ul li a").each(function () {
                            var m = d(this);
                            if (m.next("ul").length) {
                                m.append('<i class="sub-menu-arrow ti-angle-right"></i>')
                            }
                        })
                    }, 200)
                });
                d(document).on("click", '[data-action="navigation-toggler"]', function () {
                    if (e.hasClass("horizontal-navigation")) {
                        d(".horizontal-navigation").toggleClass("open")
                    } else {
                        d(".navigation").toggleClass("open")
                    }
                    d.createOverlay()
                });
                d(document).on("click", "[data-nav-target]", function () {
                    var m = d(this), n = m.data("nav-target");
                    if (e.hasClass("navigation-toggle-one")) {
                        e.addClass("navigation-show")
                    }
                    if (e.hasClass("horizontal-navigation")) {
                        d(".navigation .navigation-menu-body").show()
                    }
                    d(".navigation .navigation-menu-body .navigation-menu-group > div").removeClass("open");
                    d(".navigation .navigation-menu-body .navigation-menu-group " + n).addClass("open");
                    d("[data-nav-target]").removeClass("active");
                    m.addClass("active");
                    m.tooltip("hide");
                    return false
                });
                var f = d(".header .header-left .header-logo").clone();
                d(".navigation .navigation-header").append(f.addClass("navigation-logo").removeClass("header-logo"));
                d(document).on("click", ".navigation-toggler a", function () {
                    if (l.width() < 1200) {
                        d.createOverlay();
                        e.addClass("navigation-show")
                    } else {
                        if (!e.hasClass("navigation-toggle-one") && !e.hasClass("navigation-toggle-two")) {
                            e.addClass("navigation-toggle-one")
                        } else {
                            if (e.hasClass("navigation-toggle-one") && !e.hasClass("navigation-toggle-two")) {
                                e.addClass("navigation-toggle-two");
                                e.removeClass("navigation-toggle-one")
                            } else {
                                if (!e.hasClass("navigation-toggle-one") && e.hasClass("navigation-toggle-two")) {
                                    e.removeClass("navigation-toggle-two");
                                    e.removeClass("navigation-toggle-one")
                                }
                            }
                        }
                    }
                    return false
                });
                d(document).on("click", ".header-toggler a", function () {
                    d(".header ul.navbar-nav").toggleClass("open");
                    return false
                });
                d(document).on("click", "*", function (m) {
                    if (!d(m.target).is(d(".navigation, .navigation *, .navigation-toggler *")) && e.hasClass("navigation-toggle-one")) {
                        e.removeClass("navigation-show")
                    }
                });
                d(document).on("click", "*", function (m) {
                    if (!d(m.target).is(".header ul.navbar-nav, .header ul.navbar-nav *, .header-toggler, .header-toggler *")) {
                        d(".header ul.navbar-nav").removeClass("open")
                    }
                });
                var k = d(".table-responsive-stack");
                k.find("th").each(function (m) {
                    d(".table-responsive-stack td:nth-child(" + (m + 1) + ")").prepend('<span class="table-responsive-stack-thead">' + d(this).text() + ":</span> ");
                    d(".table-responsive-stack-thead").hide()
                });
                k.each(function () {
                    var n = d(this).find("th").length, m = 100 / n + "%";
                    d(this).find("th, td").css("flex-basis", m)
                });

                function i() {
                    if (l.width() < 768) {
                        d(".table-responsive-stack").each(function (m) {
                            d(this).find(".table-responsive-stack-thead").show();
                            d(this).find("thead").hide()
                        })
                    } else {
                        d(".table-responsive-stack").each(function (m) {
                            d(this).find(".table-responsive-stack-thead").hide();
                            d(this).find("thead").show()
                        })
                    }
                }

                i();
                window.onresize = function (m) {
                    i()
                };
                d(document).on("click", '[data-toggle="search"], [data-toggle="search"] *', function () {
                    d(".header .header-body .header-search").show().find(".form-control").focus();
                    return false
                });
                d(document).on("click", ".close-header-search, .close-header-search svg", function () {
                    d(".header .header-body .header-search").hide();
                    return false
                });
                d(document).on("click", "*", function (m) {
                    if (!d(m.target).is(d('.header, .header *, [data-toggle="search"], [data-toggle="search"] *'))) {
                        d(".header .header-body .header-search").hide()
                    }
                });
                d(document).on("click", ".accordion.custom-accordion .accordion-row a.accordion-header", function () {
                    var m = d(this);
                    m.closest(".accordion.custom-accordion").find(".accordion-row").not(m.parent()).removeClass("open");
                    m.parent(".accordion-row").toggleClass("open");
                    return false
                });
                var h, j = d(".table-responsive");
                j.on("show.bs.dropdown", function (m) {
                    h = d(m.target).find(".dropdown-menu");
                    e.append(h.detach());
                    var n = d(m.target).offset();
                    h.css({
                        display: "block",
                        top: n.top + d(m.target).outerHeight(),
                        left: n.left,
                        width: "184px",
                        "font-size": "14px"
                    });
                    h.addClass("mobPosDropdown")
                });
                j.on("hide.bs.dropdown", function (m) {
                    d(m.target).append(h.detach());
                    h.hide()
                });
                d(document).on("click", ".chat-block .chat-sidebar .chat-sidebar-content .list-group .list-group-item", function () {
                    d(".chat-block .chat-content").addClass("chat-mobile-open");
                    return false
                });
                d(document).on("click", ".chat-block .chat-content .mobile-chat-close-btn a", function () {
                    d(".chat-block .chat-content").removeClass("chat-mobile-open");
                    return false
                });
                d(document).on("click", ".navigation ul li a", function () {
                    var m = d(this);
                    if (m.next("ul").length) {
                        var n = m.find(".sub-menu-arrow");
                        n.toggleClass("fa-rotate-90");
                        m.next("ul").toggle(200);
                        m.parent("li").siblings().find("ul").not(m.parent("li").find("ul")).slideUp(200);
                        m.next("ul").find("li ul").slideUp(200);
                        m.next("ul").find("li>a").find(".sub-menu-arrow").removeClass("ti-minus").addClass("ti-plus");
                        m.next("ul").find("li>a").find(".sub-menu-arrow").removeClass("rotate-in");
                        m.parent("li").siblings().not(m.parent("li").find("ul")).find(">a").find(".sub-menu-arrow").removeClass("ti-minus").addClass("ti-plus");
                        m.parent("li").siblings().not(m.parent("li").find("ul")).find(">a").find(".sub-menu-arrow").removeClass("rotate-in");
                        if (n.hasClass("rotate-in")) {
                            setTimeout(function () {
                                n.removeClass("ti-plus").addClass("ti-minus")
                            }, 200)
                        } else {
                            n.removeClass("ti-minus").addClass("ti-plus")
                        }
                        if (!e.hasClass("horizontal-side-menu") && l.width() >= 1200) {
                            setTimeout(function (o) {
                                d(".navigation .navigation-menu-body").getNiceScroll().resize()
                            }, 300)
                        }
                        return false
                    }
                });
                d(document).on("click", ".horizontal-navigation ul li a", function () {
                    var m = d(this);
                    if (m.next("ul").length) {
                        m.next("ul").toggle(200);
                        m.parent("li").siblings().find("ul").not(m.parent("li").find("ul")).slideUp(200);
                        m.next("ul").find("li ul").slideUp(200);
                        return false
                    }
                });
                d(document).on("click", ".dropdown-menu", function (m) {
                    m.stopPropagation()
                });
                d('[data-toggle="tooltip"]').tooltip({container: "body"});
                d('[data-toggle="popover"]').popover();
                d(".carousel").carousel();
                /*if (l.width() >= 992) {
                    d(".card-scroll").niceScroll();
                    d(".table-responsive").niceScroll();
                    d(".sidebar-group .sidebar").niceScroll();
                    d(".app-block .app-content .app-lists").niceScroll();
                    d(".app-block .app-sidebar .app-sidebar-menu").niceScroll();
                    d(".chat-block .chat-sidebar .chat-sidebar-content").niceScroll();
                    var g = d(".chat-block .chat-content .messages");
                    if (g.length) {
                        g.niceScroll({horizrailenabled: false});
                        g.getNiceScroll(0).doScrollTop(g.get(0).scrollHeight, -1)
                    }
                }
                if (!e.hasClass("small-navigation") && !e.hasClass("horizontal-navigation") && l.width() >= 992) {
                    d(".navigation .navigation-menu-body").niceScroll()
                }
                d(".dropdown-menu ul.list-group").niceScroll()*/
            })(jQuery)
        }), 0:
    /******************************************************************!*\
     !***
     \*****************************************************************/
    /* no static exports found */
        (function (c, b, a) {
            a(
                /* C:\wamp64\www\themeforest\nago\resources\js\app.js */
                "./resources/js/app.js");
            c.exports = a(
                /* C:\wamp64\www\themeforest\nago\public\assets\sass\app.scss */
                "./public/assets/sass/app.scss")
        })
});