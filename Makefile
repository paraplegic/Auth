## use the BASH shell 
SHELL=/usr/local/bin/bash

## local resources
WORK_DIR=./app
SOURCE_DIR=./src
DEPS=./requirements.txt
MODEL=../resources/model
ENV=./resources/test
USR_CFG=$(MODEL)/users.yml
TDIR=./data
BKP=./backup.tgz

TESTS=test_config test_persist test_model test_sql test_sqlite

all:	test

$(WORK_DIR):
	python3 -m venv $(WORK_DIR)

init: $(WORK_DIR)
	## cd $(WORK_DIR); . bin/activate ; pip install --upgrade pip 
	cd $(WORK_DIR); . bin/activate ; pip install --log /tmp/pip.log -r ../$(DEPS)

update:
	cp -r $(SOURCE_DIR) $(WORK_DIR)
	cp -r $(ENV) $(WORK_DIR)

test_clean:
	rm -rf $(TDIR)/*.sq3

clean:	test_clean
	@echo himom

realclean: clean
	rm -rf $(WORK_DIR)

backup:
	tar -zcvf $(BKP) ./

run:
	@echo ::: ERROR: $@ not implemented

test_config:
	@echo ===========
	@echo config
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; python3 $(SOURCE_DIR)/Config.py $(USR_CFG)

test_persist:
	@echo ===========
	@echo persistence
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; python3 $(SOURCE_DIR)/Persist.py $(USR_CFG)

test_model:
	@echo ===========
	@echo model
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; python3 $(SOURCE_DIR)/Model.py $(USR_CFG)

test_sql:
	@echo ===========
	@echo Sql
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; python3 $(SOURCE_DIR)/Sql.py $(USR_CFG)

test_sqlite:
	@echo ===========
	@echo Sqlite
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; python3 $(SOURCE_DIR)/Sqlite.py $(USR_CFG)

test: update $(TESTS) 
