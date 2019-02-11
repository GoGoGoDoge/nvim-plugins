import pynvim

@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('PrettyGherkin', nargs='*', range='')
    def PrettyGherkin(self, args, range):
        """Format the current opening vim window to a pretty Gherkin style.
        Prerequisite:
        1. This plugin does not check your Gherkin file.
        2. It does pretty formatting on its best effort.
        """
        # line = self.nvim.current.buffer.line_count()
        buf = self.nvim.current.buffer
        # line = self.nvim.current.buffer.line_count()
        formatted_content = self.pretty_gherkin_util(buf)
        del buf[:]
        self.nvim.current.buffer.append(formatted_content[:-1], 0)
        self.nvim.current.line = formatted_content[-1]
        # for i, line in enumerate(formatted_content):
        #     if i == 0:
        #         self.nvim.current.buffer.append(line, i)
        #     else:
        #         self.nvim.current.buffer.append(line)
        self.nvim.api.out_write('Pretty Gerkin Done...')
        self.nvim.api.out_write('Please check FIX THIS LINE if necessary...')
        # self.nvim.current.line = ('' + str(line))
        # self.nvim.current.line = ('Command with args: {}, range: {}'
        #                           .format(args, range))

    def pretty_gherkin_util(self, buf):
        content = []
        tables = []
        for line in buf:
            words = line.strip().split()
            if len(words) == 0:
                continue
            if words[0][0] == '|':
                tables.append(line.strip())
                continue
            # flushing tables into content
            if len(tables) > 0:
                tables = self.prettify(tables)
                for row in tables:
                    content.append('\t\t\t' + "".join(row))
                del tables[:]
            if words[0] == 'Feature:':
                content.append(self.feature(words))
            elif words[0][0] == '@':
                content.append("")
                content.append('\t' + ''.join(self.feature(words)))
            elif words[0] == 'Background:' or words[0] == 'Scenario':
                content.append('\t' + ''.join(self.feature(words)))
            elif words[0] == 'Given' or words[0] == 'And' or words[0] == 'Then' or words[0] == 'Examples:' or words[0] == 'When':
                content.append('\t\t' + ''.join(self.feature(words)))
            elif words[0][0] == '#':  # This is comment. Do nothing.
                content.append(line)
            else:
                content.append('======> FIX THIS LINE =====>' + ''.join(words))

        if len(tables) > 0:
            tables = self.prettify(tables)
            for row in tables:
                content.append('\t\t\t' + "".join(row))
            del tables[:]

        return content

    def feature(self, words):
        res = []
        for word in words:
            res.append(word.strip() + ' ')
        return ''.join(res).strip()

    def prettify(self, tables):
        rows = []
        for line in tables:
            rows.append(self.clean(line))
        # Use first row as reference to do alignment.
        if len(rows) == 0:
            return rows

        col_len = len(rows[0])
        for j in range(col_len):
            max_len = 0
            for line in rows:
                if j < len(line):
                    max_len = max(max_len, len(line[j]))
            for i, line in enumerate(rows):
                if j < len(line):
                    s = line[j].ljust(max_len)
                    rows[i][j] = ' %s |' % s
        for i, line in enumerate(rows):
            if len(line) > 0:
                rows[i][0] = '|' + line[0]

        return rows

    def clean(self, line):
        words = line.split('|')
        res = []
        for word in words:
            if len(word) > 0:
                res.append(word.strip())
        return res
