=======
History
=======

0.1.0 (2019-02-19)
------------------

* Initial release. Not working. Do not use.

0.2.0 (2019-02-19)
------------------

* Initial release. Not working. Do not use.

0.3.0 (2019-02-19)
------------------

* First working release on PyPI.

0.4.8 (2019-02-20)
------------------

* Fix travis deploy repo, once more.

0.4.9 (2019-02-20)
------------------

* Fix README formatting for docs.

0.4.10 (2019-02-20)
-------------------

* Fix links to github repo

0.4.11 (2019-02-20)
-------------------

* Updated usage in README.

0.4.12 (2019-02-20)
-------------------

* Fix typo in README.

0.4.13 (2019-02-20)
-------------------

* Fix README parse issue.

1.0.0 (2019-02-21)
------------------

* Updated to return all device information.
* Added extra unit tests.

1.0.1 (2019-02-22)
------------------

* Minor bug fixes and extra unit tests

1.0.2 (2019-02-22)
------------------

* Logging fixes around token refresh

1.0.3 (2019-02-22)
------------------

* Fix History.rst formatting issue.

1.0.4 (2019-02-22)
------------------

* Take SSL param in init now
* Fix some typos

1.0.5 (2019-02-24)
------------------

* As a convenience, as the router IP as the host
  for every device. Can be useful when a network has more
  than one router.

1.0.6 (2019-02-26)
------------------

* Only a docs update.

1.0.7 (2019-02-26)
------------------

* Only a docs update.


1.1.0 (2019-07-16)
------------------

* Compatibility with 15.05.


1.1.1 (2019-09-19)
------------------

* Adding packaging dependancy.

1.1.2 (2019-10-11)
------------------

* Add option to enable or disable HTTPS verification.
* Suppress "InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised." warnings.
* Reduce number of info log messages.
* Minor code clean-up to address flake8 warnings.


1.1.3 (2020-04-20)
------------------
* Add packaging


1.1.5 (2020-09-01)
------------------
* Unpin pip versions. Allow higher. Fixes #42 https://github.com/fbradyirl/openwrt-luci-rpc/issues/42


1.1.6 (2020-09-01)
------------------
* Fixes home-assistant/core/issues/38870, home-assistant/core/issues/39498
* Fixes fbradyirl/openwrt-luci-rpc/issues/33

1.1.7 (2020-12-08)
------------------
* Switch pipeline to Github actions

1.1.8 (2021-03-12)
------------------
* Support newer openwrt snapshot versions (#45)
* Fix tox in github actions and also test py38 (#46)

1.1.9 (2021-03-21)
------------------
* Publish to pypi only once in github actions (#47)

1.1.10 (2021-03-21)
-------------------
* Also trigger the Github Actions on push of tags (#49)

1.1.11 (2021-03-21)
-------------------
* Add rst-linter pre-commit hook to prevent committing errors to HISTORY.rst #50


1.1.12 (2022-09-11)
-------------------
* Includes latest fixes to support newer versions of OpenWrt
