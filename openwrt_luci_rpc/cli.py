# -*- coding: utf-8 -*-

"""Console script for openwrt_luci_rpc."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for openwrt_luci_rpc."""
    click.echo("Replace this message by putting your code into "
               "openwrt_luci_rpc.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
