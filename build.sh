#!/bin/bash

download_link=https://github.com/ArjunSahlot/painter/archive/master.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir master.zip \
&& rm -rf master.zip \
&& mv $temporary_dir/painter-master $1/painter \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/painter[0m"
