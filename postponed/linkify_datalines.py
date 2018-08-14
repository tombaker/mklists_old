    def linkify_datalines(self):
        datalines_linkified = []
        for line in self.datalines:
            if '<a href=' in line:
                return line
            line = re.compile(URL_REGEX).sub(r'<a href="\1">\1</a>', string)
            datalines_linkified.append

    
