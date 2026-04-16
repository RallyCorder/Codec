pkgname=codec-widget
pkgver=1.0
pkgrel=1
pkgdesc="Widget assistant with visual feedback for repetitive tasks"
url="https://github.com/RallyCorder/Codec"
arch=(x86_64)
license=('MIT-0')
depends=(
  python
  pyside6
)
makedepends=(
  git
  python-build
  python-installer
  python-wheel
)
optdepends=(
    adwaita-qt6
    python-paramiko
)
source=("git+https://github.com/RallyCorder/Codec.git")

sha256sums=('SKIP')

build() {
  cd Codec
  python -m build
}

package() {
  cd Codec
  python -m installer --destdir="$pkgdir" dist/*.whl
}