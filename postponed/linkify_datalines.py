    def linkify(lines):
        datalines_linkified = []
        for line in lines:
            if '<a href=' in line:
                return line
            line = re.compile(URL_REGEX).sub(r'<a href="\1">\1</a>', string)
            datalines_linkified.append(line)

        return lines_linkified

    
