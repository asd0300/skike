(() => {
  "use strict";
  const t = new (class {
    constructor() {
      (this.API_HOST = "https://api.appworks-school.tw/api/1.0"),
        (this.accessToken = void 0);
    }
    getProducts(t, e) {
      return fetch(`${this.API_HOST}/products/${t}?paging=${e}`).then((t) =>
        t.json()
      );
    }
    getCampaigns() {
      return fetch(`${this.API_HOST}/marketing/campaigns`).then((t) =>
        t.json()
      );
    }
    searchProducts(t, e) {
      return fetch(
        `${this.API_HOST}/products/search?keyword=${t}&paging=${e}`
      ).then((t) => t.json());
    }
    getProduct(t) {
      return fetch(`${this.API_HOST}/products/details?id=${t}`).then((t) =>
        t.json()
      );
    }
    checkout(t) {
      return this.accessToken
        ? fetch(`${this.API_HOST}/order/checkout`, {
            body: JSON.stringify(t),
            headers: new Headers({
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.accessToken}`,
            }),
            method: "POST",
          }).then((t) => {
            if (401 === t.status) throw new Error("請先登入");
            if (403 === t.status) throw new Error("內容錯誤或權限不足");
            return t.json();
          })
        : Promise.reject(new Error("請先登入"));
    }
    signin(t) {
      return fetch(`${this.API_HOST}/user/signin`, {
        body: JSON.stringify(t),
        headers: new Headers({ "Content-Type": "application/json" }),
        method: "POST",
      }).then((t) =>
        t.json().then((t) => ((this.accessToken = t.data.access_token), t))
      );
    }
  })();
  new (class extends class {
    constructor(t, e, s, i) {
      (this.model = t),
        (this.view = e),
        (this.fb = s),
        (this.tappay = i),
        this.view.bindInputSearchPressEnter(this.redirectToIndexPageWithTag),
        this.view.bindClickProfile(this.handleClickProfile.bind(this));
    }
    init() {
      this.view.handleTag(this.paramsTag),
        this.view.renderCount(this.model.cart.items.length);
    }
    get paramsNumber() {
      return this.getParams("number");
    }
    get paramsId() {
      return this.getParams("id");
    }
    get paramsTag() {
      return this.getParams("tag") || "all";
    }
    getParams(t) {
      return new URLSearchParams(window.location.search).get(t);
    }
    redirectToIndexPageWithTag(t) {
      window.location.href = `/?tag=${t}`;
    }
    handleClickProfile() {
      this.fb.jwtToken
        ? (window.location.href = "/profile.html")
        : this.fb
            .login()
            .then((t) => this.fb.handleLoginStatus(t))
            .then((t) => {
              t && window.alert("登入成功！");
            });
    }
  } {
    constructor(t, e, s, i) {
      super(t, e, s, i),
        (this.nextPaging = 0),
        (this.isFetching = !1),
        (this.interval = void 0),
        (this.intervalTime = 5e3),
        this.view.bindScrollToBottom(this.getMoreProducts.bind(this));
    }
    init() {
      super.init(), this.fb.init(), this.getCampaigns(), this.getMoreProducts();
    }
    get isPredefinedTag() {
      return (
        ["women", "men", "accessories", "all"].indexOf(this.paramsTag) > -1
      );
    }
    getMoreProducts() {
      this.isFetching ||
        void 0 === this.nextPaging ||
        ((this.isFetching = !0),
        (this.isPredefinedTag
          ? t.getProducts(this.paramsTag, this.nextPaging)
          : t.searchProducts(this.paramsTag, this.nextPaging)
        ).then(({ data: t, next_paging: e }) => {
          (this.isFetching = !1),
            (this.nextPaging = e),
            this.model.setProducts(t),
            this.onProductsChanged(this.model.products);
        }));
    }
    getCampaigns() {
      t.getCampaigns().then(({ data: t }) => {
        this.model.setCampaigns(t),
          this.onCampaignsChanged(
            this.model.campaigns,
            this.model.activeCampaignIndex
          ),
          this.setupInterval();
      });
    }
    onProductsChanged(t) {
      0 === t.length
        ? this.view.renderNoProductsText()
        : this.view.renderProducts(t);
    }
    onCampaignsChanged(t, e) {
      this.view.renderCampaigns(t),
        this.view.setActiveCampaign(e),
        this.view.bindClickDot(this.handleClickDot.bind(this));
    }
    onActiveCampaignChanged(t) {
      this.view.setActiveCampaign(t);
    }
    handleClickDot(t) {
      this.model.setActiveCampaignIndex(t),
        this.onActiveCampaignChanged(this.model.activeCampaignIndex),
        this.setupInterval();
    }
    handleInterval() {
      this.model.setNextActiveCampaignIndex(),
        this.onActiveCampaignChanged(this.model.activeCampaignIndex);
    }
    setupInterval() {
      this.interval && clearInterval(this.interval),
        (this.interval = window.setInterval(
          this.handleInterval.bind(this),
          this.intervalTime
        ));
    }
  })(
    new (class extends class {
      constructor(t) {
        this.cart = t;
      }
    } {
      constructor(t) {
        super(t),
          (this.products = []),
          (this.campaigns = []),
          (this.activeCampaignIndex = 0);
      }
      setProducts(t) {
        this.products = t;
      }
      setCampaigns(t) {
        this.campaigns = t;
      }
      setActiveCampaignIndex(t) {
        this.activeCampaignIndex = t;
      }
      setNextActiveCampaignIndex() {
        const t = this.activeCampaignIndex,
          e = t + 1 === this.campaigns.length ? 0 : t + 1;
        this.activeCampaignIndex = e;
      }
    })(
      new (class {
        constructor() {
          this.items = JSON.parse(window.localStorage.getItem("cart") || "[]");
        }
        static calculateSubtotal(t) {
          return t.reduce((t, e) => t + e.qty * e.price, 0);
        }
        update() {
          window.localStorage.setItem("cart", JSON.stringify(this.items));
        }
      })()
    ),
    new (class extends class {
      constructor() {
        (this.tagMen = this.getElement(".tag-men")),
          (this.tagWomen = this.getElement(".tag-women")),
          (this.tagAccessories = this.getElement(".tag-accessories")),
          (this.desktopInputSearch = this.getElement(
            ".desktop-header .search"
          )),
          (this.mobileInputSearch = this.getElement(".mobile-header .search")),
          (this.desktopMember = this.getElement(".desktop-header .member")),
          (this.mobileMember = this.getElement(".mobile-footer .member")),
          (this.desktopCount = this.getElement(".desktop-header .count")),
          (this.mobileCount = this.getElement(".mobile-footer .count"));
      }
      createElement(t, e) {
        const s = document.createElement(t);
        return (
          e.classList && s.classList.add(...e.classList),
          e.attributes &&
            Object.entries(e.attributes).forEach(([t, e]) => {
              s.setAttribute(t, e);
            }),
          e.styles &&
            Object.entries(e.styles).forEach(([t, e]) => {
              s.style[t] = e;
            }),
          e.children && s.append(...e.children),
          e.parent && e.parent.append(s),
          s
        );
      }
      getElement(t) {
        return document.querySelector(t);
      }
      handleTag(t) {
        switch (t) {
          case "men":
            this.tagMen.classList.add("tag--active");
            break;
          case "women":
            this.tagWomen.classList.add("tag--active");
            break;
          case "accessories":
            this.tagAccessories.classList.add("tag--active");
            break;
          case "all":
            break;
          default:
            (this.desktopInputSearch.value = t),
              (this.mobileInputSearch.value = t);
        }
      }
      bindInputSearchPressEnter(t) {
        this.desktopInputSearch.addEventListener("keydown", (e) => {
          13 === e.keyCode && t(e.currentTarget.value);
        }),
          this.mobileInputSearch.addEventListener("keydown", (e) => {
            13 === e.keyCode && t(e.currentTarget.value);
          });
      }
      bindClickProfile(t) {
        this.desktopMember.addEventListener("", () => {
          t();
        }),
          this.mobileMember.addEventListener("", () => {
            t();
          });
      }
      renderCount(t) {
        (this.desktopCount.textContent = t), (this.mobileCount.textContent = t);
      }
    } {
      constructor() {
        super(),
          (this.scrollToBottomOffset = 240),
          (this.products = this.getElement("#products")),
          (this.noProducts = this.getElement("#no-products")),
          (this.campaigns = this.getElement("#campaigns")),
          (this.campaignList = []),
          (this.dotList = []);
      }
      renderProducts(t) {
        t.forEach((t) => {
          this.createElement("a", {
            classList: ["product"],
            // attributes: { href: `/product.html?id=${t.id}` },
            parent: this.products,
            children: [
              this.createElement("img", { attributes: { src: t.main_image } }),
              this.createElement("div", {
                classList: ["product__colors"],
                children: t.colors.map((t) =>
                  this.createElement("div", {
                    classList: ["product__color"],
                    styles: { backgroundColor: `#${t.code}` },
                  })
                ),
              }),
              this.createElement("div", {
                classList: ["product__title"],
                children: [t.title],
              }),
              this.createElement("div", {
                classList: ["product__price"],
                children: [`TWD.${t.price}`],
              }),
            ],
          });
        });
      }
      renderNoProductsText() {
        this.createElement("h2", {
          parent: this.noProducts,
          children: ["搜尋不到產品喔"],
        });
      }
      renderCampaigns(t) {
        (this.campaigns.innerHTML = ""),
          (this.campaignList = t.map((t) =>
            this.createElement("a", {
              classList: ["campaign"],
              styles: { backgroundImage: `url(${t.picture})` },
              // attributes: { href: `/product.html?id=${t.product_id}` },
              parent: this.campaigns,
              children: [
                this.createElement("div", {
                  classList: ["campaign__story"],
                  children: [t.story],
                }),
              ],
            })
          )),
          (this.dotList = t.map(() =>
            this.createElement("div", { classList: ["dot"] })
          )),
          this.createElement("div", {
            classList: ["dots"],
            parent: this.campaigns,
            children: this.dotList,
          });
      }
      setActiveCampaign(t) {
        this.campaignList.forEach((e, s) => {
          e.classList.remove("campaign--active"),
            s === t && e.classList.add("campaign--active");
        }),
          this.dotList.forEach((e, s) => {
            e.classList.remove("dot--active"),
              s === t && e.classList.add("dot--active");
          });
      }
      bindClickDot(t) {
        this.dotList.forEach((e, s) => {
          e.addEventListener("click", () => {
            t(s);
          });
        });
      }
      bindScrollToBottom(t) {
        window.addEventListener("scroll", () => {
          document.body.getBoundingClientRect().bottom - window.innerHeight <
            this.scrollToBottomOffset && t();
        });
      }
    })(),
    new (class {
      constructor() {
        this.jwtToken = void 0;
      }
      loadSdk() {
        return new Promise((t) => {
          var e, s, i, a, n;
          (window.fbAsyncInit = () => {
            t();
          }),
            (s = "script"),
            (i = "facebook-jssdk"),
            (n = (e = document).getElementsByTagName(s)[0]),
            e.getElementById(i) ||
              (((a = e.createElement(s)).id = i),
              (a.src = "https://connect.facebook.net/zh_TW/sdk.js"),
              n.parentNode.insertBefore(a, n));
        });
      }
      init() {
        return this.loadSdk()
          .then(
            () => (
              window.FB.init({
                appId: "700590737403665",
                cookie: !0,
                xfbml: !0,
                version: "v10.0",
              }),
              this.getLoginStatus()
            )
          )
          .then((t) => this.handleLoginStatus(t));
      }
      getLoginStatus() {
        return new Promise((t) => {
          window.FB.getLoginStatus((e) => {
            t(e);
          });
        });
      }
      login() {
        return new Promise((t) => {
          window.FB.login(
            (e) => {
              t(e);
            },
            { scope: "public_profile,email" }
          );
        });
      }
      handleLoginStatus(e) {
        return "connected" === e.status
          ? t
              .signin({
                provider: "facebook",
                access_token: e.authResponse.accessToken,
              })
              .then(({ data: t }) => ((this.jwtToken = t.access_token), t.user))
          : Promise.resolve();
      }
      logout() {
        return new Promise((t) => {
          window.FB.logout(() => {
            t();
          });
        });
      }
    })(),
    new (class {
      constructor() {
        (this.appId = "12348"),
          (this.appKey =
            "app_pa1pQcKoY22IlnSXq5m5WP5jFKzoRG58VEXpT7wU62ud7mMbDOGzCYIlzzLF"),
          (this.serverType = "sandbox");
      }
      setupSdk() {
        window.TPDirect.setupSDK(this.appId, this.appKey, this.serverType);
      }
      setupCard() {
        window.TPDirect.card.setup({
          fields: {
            number: {
              element: "#card-number",
              placeholder: "**** **** **** ****",
            },
            expirationDate: {
              element: "#card-expiration-date",
              placeholder: "MM / YY",
            },
            ccv: { element: "#card-ccv", placeholder: "後三碼" },
          },
          styles: {
            ".valid": { color: "green" },
            ".invalid": { color: "red" },
          },
        });
      }
      init() {
        this.setupSdk(), this.setupCard();
      }
      getPrime() {
        return new Promise((t) => {
          window.TPDirect.card.getPrime((e) => {
            0 === e.status && t(e.card.prime);
          });
        });
      }
      get canGetPrime() {
        return window.TPDirect.card.getTappayFieldsStatus().canGetPrime;
      }
      get cannotGetPrimeReason() {
        const t = window.TPDirect.card.getTappayFieldsStatus();
        return 1 === t.status.number
          ? "請輸入信用卡號碼"
          : 2 === t.status.number
          ? "信用卡號碼有誤"
          : 1 === t.status.expiry
          ? "請輸入有效期限"
          : 2 === t.status.expiry
          ? "有效期限有誤"
          : 1 === t.status.ccv
          ? "請輸入安全碼"
          : 2 === t.status.ccv
          ? "安全碼有誤"
          : void 0;
      }
    })()
  ).init();
})();
