import re

import aioreactive as rx

from core.settings import settings


def build_re(words: list[str]):
    return '((' + '|'.join(words) + ')' + r' *[:=] *[\'"][^\"]{4,50}[\'"])'


class ExposedKeysFinder(rx.AsyncSubject):
    def __init__(self, filter_by_key: str):
        super().__init__()
        self.re = build_re([filter_by_key])

    async def asend(self, item):
        content = item['content']
        matches = re.findall(self.re, content)
        matches = [m[0] for m in matches]
        if len(matches) > 0:
            print(f'found {len(matches)=} exposed keys')
            return await super().asend({
                'html_url': item['html_url'],
                'sha': item['sha'],
                'matches': matches,
            })


class PrinterSubject(rx.AsyncSubject):
    async def asend(self, item):
        print('PrinterSubject')
        return await super().asend(item)


async def observable_from_several_words(words: list[str]):
    subj = PrinterSubject()
    if len(words) == 0:
        for word_subj in subjects.values():
            print('sub', word_subj)
            await word_subj.subscribe_async(subj)
    else:
        for word in words:
            print('sub', word)
            if word in subjects.keys():
                await subjects[word].subscribe_async(subj)
    return subj


subjects = {word: ExposedKeysFinder(word) for word in settings.SEARCH_KEYWORDS}
