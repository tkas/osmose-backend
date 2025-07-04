#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Name_MisspelledWordByRegex_Lang_fa(PluginMapCSS):
    # ------------------------------- IMPORTANT -------------------------------
    # This file is generated automatically and should not be modified directly.
    # Instead, modify the source mapcss file and regenerate this Python script.
    # -------------------------------------------------------------------------



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[50109001] = self.def_class(item = 5010, level = 2, tags = mapcss.list_('name', 'fix:chair'), title = mapcss.tr('Arabic letter detected in Farsi name'))

        self.re_4234bf3b = re.compile(r'ك')
        self.re_5eeade1c = re.compile(r'ي')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/ي/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:10/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name=",replace(tag("name"),"ي","ی"))
                # -osmoseAssertMatchWithContext:list("node name=\"روابط عمومي مجتمع مس شهربابك\"","language=fa")
                # assertNoMatch:"node name=\"روابط عمومي مجتمع مس شهربابك\""
                err.append({'class': 50109001, 'subclass': 10, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name:fa=~/ي/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:11/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ي","ی"))
                # assertMatch:"node name:fa=\"روابط عمومي مجتمع مس شهربابك\""
                err.append({'class': 50109001, 'subclass': 11, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name=~/ك/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:20/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name=",replace(tag("name"),"ك","ک"))
                # -osmoseAssertMatchWithContext:list("node name=\"روابط عمومي مجتمع مس شهربابك\"","language=fa")
                # assertNoMatch:"node name=\"روابط عمومي مجتمع مس شهربابك\""
                err.append({'class': 50109001, 'subclass': 20, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ك', 'ک'))).split('=', 1)])
                }})

        # *[name:fa=~/ك/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:21/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ك","ک"))
                # assertMatch:"node name:fa=\"روابط عمومي مجتمع مس شهربابك\""
                err.append({'class': 50109001, 'subclass': 21, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ك', 'ک'))).split('=', 1)])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/ي/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:10/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name=",replace(tag("name"),"ي","ی"))
                err.append({'class': 50109001, 'subclass': 10, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name:fa=~/ي/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:11/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ي","ی"))
                err.append({'class': 50109001, 'subclass': 11, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name=~/ك/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:20/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name=",replace(tag("name"),"ك","ک"))
                err.append({'class': 50109001, 'subclass': 20, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ك', 'ک'))).split('=', 1)])
                }})

        # *[name:fa=~/ك/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:21/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ك","ک"))
                err.append({'class': 50109001, 'subclass': 21, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ك', 'ک'))).split('=', 1)])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/ي/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:10/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name=",replace(tag("name"),"ي","ی"))
                err.append({'class': 50109001, 'subclass': 10, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name:fa=~/ي/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5eeade1c), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:11/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ي","ی")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ي","ی"))
                err.append({'class': 50109001, 'subclass': 11, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ي', 'ی'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ي', 'ی'))).split('=', 1)])
                }})

        # *[name=~/ك/][language("fa")]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.language(self.father.config.options, 'fa')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:20/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name=",replace(tag("name"),"ك","ک"))
                err.append({'class': 50109001, 'subclass': 20, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name=', mapcss.replace(mapcss.tag(tags, 'name'), 'ك', 'ک'))).split('=', 1)])
                }})

        # *[name:fa=~/ك/]
        if ('name:fa' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4234bf3b), mapcss._tag_capture(capture_tags, 0, tags, 'name:fa'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Arabic letter detected in Farsi name")
                # -osmoseItemClassLevel:"5010/50109001:21/2"
                # throwError:tr("In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.","ك","ک")
                # fixAdd:concat("name:fa=",replace(tag("name:fa"),"ك","ک"))
                err.append({'class': 50109001, 'subclass': 21, 'text': mapcss.tr('In Farsi, the Arabic letter `{0}` should be replaced by `{1}`.', 'ك', 'ک'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('name:fa=', mapcss.replace(mapcss.tag(tags, 'name:fa'), 'ك', 'ک'))).split('=', 1)])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Name_MisspelledWordByRegex_Lang_fa(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'language': 'fa'}):
            self.check_err(n.node(data, {'name': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 10})
        self.check_not_err(n.node(data, {'name': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 10})
        self.check_err(n.node(data, {'name:fa': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 11})
        with with_options(n, {'language': 'fa'}):
            self.check_err(n.node(data, {'name': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 20})
        self.check_not_err(n.node(data, {'name': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 20})
        self.check_err(n.node(data, {'name:fa': 'روابط عمومي مجتمع مس شهربابك'}), expected={'class': 50109001, 'subclass': 21})
