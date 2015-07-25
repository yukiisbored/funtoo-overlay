# Distributed under the terms of the GNU General Public License v2

EAPI=5

inherit toolchain-funcs

DESCRIPTION="User-space application to modify the EFI boot manager"
HOMEPAGE="https://github.com/vathpela/efibootmgr"
SRC_URI="https://github.com/vathpela/${PN}/releases/download/${P}/${P}.tar.bz2"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="*"
IUSE=""

RDEPEND="sys-apps/pciutils
	sys-libs/efivar"
DEPEND="${RDEPEND}"

src_prepare() {
	sed -i -e s/-Werror// Makefile || die
}

src_configure() {
	tc-export CC
	export EXTRA_CFLAGS=${CFLAGS}
}

src_install() {
	# build system uses perl, so just do it ourselves
	dosbin src/efibootmgr/efibootmgr
	doman src/man/man8/efibootmgr.8
	dodoc AUTHORS README doc/ChangeLog doc/TODO
}
