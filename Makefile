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

TESTS=test_config test_model test_sql test_sqlite test_postgres test_mysql test_persist test_html_form

all:	test

$(WORK_DIR):
	python3 -m venv $(WORK_DIR)

init: $(WORK_DIR)
	cd $(WORK_DIR); . bin/activate ; pip install --upgrade pip 
	cd $(WORK_DIR); . bin/activate ; pip install --log /tmp/pip.log -r ../$(DEPS)

update:
	cp -r $(SOURCE_DIR) $(WORK_DIR)
	cp -r $(ENV) $(WORK_DIR)

test_clean:
	rm -rf $(TDIR)/test
	psql -h lifter -d test -U rob < $(TDIR)/dropall.sql
	mysql -h lifter -p test < $(TDIR)/dropall.sql

clean:	test_clean
	@echo himom

realclean: clean
	rm -rf $(WORK_DIR)

backup:
	tar -zcvf $(BKP) ./

test_config:
	@echo ===========
	@echo config
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; python3 $(SOURCE_DIR)/Config.py $(USR_CFG)

test_persist:
	@echo ===========
	@echo persistence sqlite
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; python3 src/Persist.py $(USR_CFG) sqlite
	@echo ===========
	@echo persistence postgres
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; python3 src/Persist.py $(USR_CFG) postgres
	@echo ===========
	@echo persistence mysql
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; export DBMS_PORT=3306; python3 src/Persist.py $(USR_CFG) mysql

test_model:
	@echo ===========
	@echo model
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; python3 $(SOURCE_DIR)/Model.py $(USR_CFG) sqlite

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

test_postgres:
	@echo ===========
	@echo PostgreSQL
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; python3 $(SOURCE_DIR)/Postgres.py $(USR_CFG)

test_mysql:
	@echo ===========
	@echo MySql
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; export DBMS_PORT=3306; python3 $(SOURCE_DIR)/MySql.py $(USR_CFG)

test_html_form:
	@echo ===========
	@echo Form
	@echo ===========
	@cd $(WORK_DIR);. ./bin/activate ; . ./test/env.sh; export DBMS_PORT=3306; python3 $(SOURCE_DIR)/HtmlForm.py $(USR_CFG)

test: update $(TESTS) 

run:	update
	cd $(WORK_DIR)/src;. ../bin/activate ; . ../test/env.sh; uvicorn main:app --reload --host 0.0.0.0 --port 8002
