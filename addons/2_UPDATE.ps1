param(
$REPO="d:/sepius/seppius-xbmc-repo"
)
chcp 65001
cd $REPO\trunk\addons
ipy ./addons_xml_generator.py
cd ../..
echo STATUS...
svn status
svn add --force *
svn status