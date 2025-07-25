PYFILES=$(shell find .. ! -path ./venv -name '*.py' -not -type l | grep -v 'Josm_' | grep -v 'disabled' | grep -v 'plugins/tests' | sort)
JSON=$(shell find ../merge_data -name '*.json' | sort)

PO:=$(wildcard *.po)

.PRECIOUS: $(PO)

all: osmose-backend.pot %.po josm_po

tmp.json: $(JSON) Makefile
	for json in $(JSON); do cat $$json | jq -r '.[].title' | grep -v 'null' | sed -e 's/\(.*\)/_("\1")/'; done > $@

osmose-backend.pot: $(PYFILES) tmp.json
	sed -i.bak "s/^#: .*//" osmose-backend.pot
	LANG=C xgettext --join-existing -cTRANSLATORS --language=Python \
          --keyword=_ --keyword=N_ --keyword=T_ --keyword=T_f --keyword=tr \
          --force-po --omit-header --from-code=utf-8 \
          --output=$@ $(PYFILES) tmp.json

%.po:
	tx pull -a --minimum-perc=1
	@sed -i.bak 's/^# 4004.*, 2017/# 4004, 2017/' ru.po  # redact email following request

statistics:
	@for i in $(PO); do \
	  (msgfmt --statistics --verbose -o - $$i > /dev/null) 2>&1; \
	done

josm_po:
	@for i in $(PO); do \
	  sed -n '1,/^$$/p;/\.mapcss:[0-9]/,/^$$/p' josm/josm_trans/josm/$$i > josm/$$i; \
	done
