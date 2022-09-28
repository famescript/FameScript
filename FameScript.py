import os, sys


class Instance():
    def __init__(self, ins = {}):
        self.ins = {}
class Token:
    def __init__(self, name = '', value = ''):
        self.name = name
        self.value = value
        self.args = 0
        self.argname = ''
        self.varname = ''
        self.args1 = ()
    def __repr__(self):
        reprs = str(self.name) + ":" + str(self.value)
        return reprs
class Error:
    def __init__(self, name = '', value = ''):
        self.name = name
        self.value = value
        self.line = 0

class Tokenizer():
    def __init__(self, text = ''):
        self.vars = Instance()
        self.text = text
        self.func = False
        self.cfu = False
        self.pos = 0-1
        self.paren2 = False
        self.drv = ''
        self.arr = False
        self.lists = []
        self.paren = False
    def lex(self):
        tokens = []
        while self.pos < len(self.text)-1:
            self.pos += 1
            char = self.text[self.pos]
            if char in ' \t\n':
                pass
            elif char == '(':
                if self.func:
                    tokens += [Token("LPAREN")]
                else:
                    fg = Tokenizer(self.text[self.pos+1:])
                    fg.paren = True
                    fg.arr = True
                    fg.vars = self.vars
                    lex = fg.lex()
                    if lex[1] == Error:
                        return lex
                    dfs = info()
                    p = []
                    a = []
                    s = True
                    for g in lex[0]:
                        if g.name == 'SEPERATOR':
                            p += [a]
                            a = []
                            s = False
                        else:
                            a += [g]
                    if a != []:
                        p += [a]
                    if s:
                        yh = compile(lex[0], self.vars, inf = dfs)
                        if type(yh) == Error:
                            return tokens, yh

                        self.pos += fg.pos+1
                        if yh.name == '':
                            tokens += [Token("array", [])]
                        else:
                            tokens += [yh]
                    else:
                        it = []
                        for jk in p:
                            hjs = compile(jk, self.vars)
                            if type(hjs) == Error:
                                return tokens, hjs
                            it += [hjs]
                        self.pos += fg.pos+1
                        
                        tokens += [Token("array", it)]
            elif char == ')':
                if self.func:
                    tokens += [Token("RPAREN")]
                else:
                    if self.paren:
                        break
                    else:
                        return tokens, None
            elif char == '[':
                if self.func:
                    tokens += [Token("LPAREN")]
                else:
                    fg = Tokenizer(self.text[self.pos+1:])
                    fg.paren2 = True
                    fg.vars = self.vars
                    lex = fg.lex()
                    if lex[1] == Error:
                        return lex
                    dfs = info()
                    p = []
                    a = []
                    
                    m = True
                    
                    m = False
                    yh = compile(lex[0], self.vars, inf = dfs)
                    if type(yh) == Error:
                        return tokens, yh
                    self.pos += fg.pos+1
                    if yh.name != 'number':
                        return tokens, Error("SliceError", "Non-Number Type '" + yh.name + "'")
                    try:
                        int(str(yh.value))
                    except:
                        return tokens, Error("SliceError", "Non-Integer Number.")
                    tokens += [Token("slice", yh.value)]
            elif char == ']':
                if self.func:
                    tokens += [Token("RPAREN")]
                else:
                    if self.paren2:
                        break
                    else:
                        return tokens, None
            # elif char == '[':
            #     tokens += [Token("LBRACKET")]
            # elif char == ']':
            #     tokens += [Token("RBRACKET")]
            elif char == '=':
                try:
                    if self.text[self.pos+1] == '=':
                        tokens += [Token("Operator", "==")]
                        self.pos+=1
                    else:
                        tokens += [Token("ASSIGN")]
                except:
                    tokens += [Token("ASSIGN")]
            elif char == ',':
                try:
                    if False:
                        pass
                    else:
                        tokens += [Token("SEPERATOR")]
                except:
                    tokens += [Token("SEPERATOR")]
            elif char == '>':
                try:
                    if self.text[self.pos+1] == '=':
                        tokens += [Token("Operator", ">=")]
                        self.pos+=1
                    else:
                        tokens += [Token("Operator", ">")]
                except:
                    tokens += [Token("Operator", ">")]
            elif char == '<':
                try:
                    if self.text[self.pos+1] == '=':
                        tokens += [Token("Operator", "<=")]
                        self.pos+=1
                    else:
                        tokens += [Token("Operator", "<")]
                except:
                    tokens += [Token("Operator", "<")]
            elif char == '!':
                try:
                    if self.text[self.pos+1] == '=':
                        tokens += [Token("Operator", "!=")]
                        self.pos+=1
                    else:
                        return tokens, Error("IllegalCharacterError", '\'!\'')
                except:
                    tokens += [Token("Operator", "<")]
            elif char in ";":
                if self.func:
                    pass
                else:
                    return tokens, None
            elif char == '{':
                g = Tokenizer(self.text[self.pos+1:])
                g.func = True
                pl = g.lex()
                if pl[1] != None:
                    return tokens, pl[1]
                tf = ''
                ps = self.pos
                while ps < (self.pos + g.pos):
                    ps += 1
                    tf += self.text[ps]
                self.pos += g.pos+1
                tokens += [Token("section", tf)]
            

            elif char == '}':
                if self.func:
                    return tokens, None
                else:
                    return None, Error("IllegalCharacter", '\'}\'')
            elif char in '\"\'':
                val = ''
                try:
                    while (self.text[self.pos+1] != char):
                                self.pos += 1
                                val += self.text[self.pos]
                except:
                    return tokens, Error("StringError", "Unterminated String")
                self.pos += 1
                try:
                    tokens += [Token("string", eval(char + val + char))]
                except:
                    return tokens, Error("StringError", "Invaild String")
            elif char in '0123456789.':
                vm = ''
                try:
                    while self.text[self.pos] in '0123456789.':
                        vm += self.text[self.pos]
                        self.pos += 1
                        if vm.count(".") > 1:
                            return tokens, Error("NumberError", "IllegalCharacter '.'")
                except:
                    pass
                self.pos -= 1
                try:
                    tokens += [Token("number", (eval(vm)))]
                except:
                    return tokens, Error("NumberError", "IllegalCharacter '0'")
            elif char in 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM_':
                vm = ''
                fn = True
                do_func = False
                try:
                    while (self.text[self.pos] in 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM_('):
                        if self.text[self.pos] == '(':
                            fn = False
                            m = True
                            if (vm in ['if', 'while', 'for', 'try', 'function', 'return'] ):
                                fn = True
                            if ((not self.func) and (not vm in ['if', 'while', 'for', 'try', 'function', 'return'])):
                                    do_func = True
                            if (self.cfu):
                                fn = True
                                do_func = False
                                self.cfu = False
                            break

                        else:
                            vm += self.text[self.pos]
                            self.pos += 1
                except:
                    pass
                if do_func:
                                    script = Tokenizer(self.text[self.pos+1:])
                                    script.paren = True
                                    script.vars = self.vars
                                    script.func = False
                                    script.arr = True
                                    lex = script.lex()
                                    self.pos += script.pos+2
                                    if lex[1] != None:
                                        return tokens, lex[1]
                                    a = []
                                    a2 = []
                                    for item in lex[0]:
                                        if item.name == 'SEPERATOR':
                                            a += [a2]
                                            a2 = []
                                        else:
                                            a2 += [item]
                                    if a2 != []:
                                        a += [a2]
                                    exes = []
                                    if not vm in ['printf', 'system', 'scanf', 'lstrip', 'strip', 'rstrip', 'reverse', 'eval', 'int', 'float', 'str', 'string', 'type', 'var']:
                                        if not vm in self.vars.ins:
                                            return tokens, Error("UndefinedError", "Undefined '" + vm + "'")
                                    try:
                                        arr = self.vars.ins[vm].args1
                                    except:
                                        arr = Token("array", [Token("string", "")])
                                        arr.value[0].varname = "echo"
                                    vns = []
                                    y = 0-1
                                    ratd = 0-1
                                    try:
                                        for g in range(len(self.vars.ins[vm].args1.value)-len(a)):
                                            ratd += 1
                                            a += [[arr.value[(len(a)-1)+ratd]]]
                                    except:
                                        pass
                                    try:
                                        for item in a:
                                            try:
                                                y += 1
                                                ik = info()
                                                p = compile(item, self.vars, False, ik)
                                                if type(p) == Error:
                                                    return tokens, p
                                                exes += [p]
                                                self.vars.ins[arr.value[y].varname] = p
                                            except:
                                                return tokens, Error("ArgumentsError", "Need Atleast Lower Than " + str(len(self.vars.ins[vm].args1.value)))
                                    except:
                                        return tokens, Error("BuiltinsError", "builtins accept only 1 argument.")
                                    if vm in ['printf', 'system', 'scanf', 'lstrip', 'strip', 'rstrip', 'reverse', 'eval', 'int', 'float', 'str', 'string', 'type', 'var']:
                                        gch = compile([exes[0]], self.vars)
                                        if type(gch) == Error:
                                            return tokens, gch
                                    if vm == 'printf':
                                        print(gch.value, end = "")
                                        tokens += [Token("string", str(gch.value))]
                                    elif vm == 'scanf':
                                        tokens += [Token("string", input(str(gch.value)))]
                                    elif vm == 'system':
                                        os.system(str(gch.value))
                                        tokens += [Token("string", (str(gch.value)))]
                                    elif vm == 'rstrip':
                                        if not gch.name == 'string':
                                            return tokens, Error("StringToolsError", "Need A String.")
                                        gch: Token
                                        tokens += [Token("string", gch.value.rstrip())]
                                    elif vm == 'lstrip':
                                        if not gch.name == 'string':
                                            return tokens, Error("StringToolsError", "Need A String.")
                                        gch: Token
                                        tokens += [Token("string", gch.value.lstrip())]
                                    elif vm == 'strip':
                                        if not gch.name == 'string':
                                            return tokens, Error("StringToolsError", "Need A String.")
                                        gch: Token
                                        tokens += [Token("string", gch.value.strip())]
                                    elif vm == 'reverse':
                                        if not gch.name == 'string':
                                            return tokens, Error("StringToolsError", "Need A String.")
                                        gch: Token
                                        tokens += [Token("string", gch.value[::-1])]
                                    elif vm == 'eval':
                                        gch: Token
                                        fg = str(gch.value)
                                        script = Tokenizer(fg)
                                        script.vars = self.vars
                                        lex = script.lex()
                                        if lex[1] != None:
                                            return tokens, lex
                                        cf : str = compile(lex[0], self.vars)
                                        if type(cf) == Error:
                                            return tokens, cf
                                        tokens += [cf]
                                    elif vm == 'var':
                                        tokens += [Token("variable", str(gch.value))]
                                    elif vm == 'int':
                                        try:
                                            float(gch.value)
                                        except:
                                            return tokens, Error("NumberError", "Number Is Not Valid")
                                        tokens += [Token("number", int(eval(str(gch.value))))]
                                    elif vm == 'float':
                                        try:
                                            float(gch.value)
                                        except:
                                            return tokens, Error("NumberError", "Number Is Not Valid")
                                        tokens += [Token("number", float(eval(str(gch.value))))]
                                    elif vm == 'number':
                                        try:
                                            float(gch.value)
                                        except:
                                            return tokens, Error("NumberError", "Number Is Not Valid")
                                        tokens += [Token("number", (eval(str(gch.value))))]
                                    elif vm in ['string', 'str']:
                                        tokens += [Token("string", str((gch.value)))]
                                    elif vm in ['type']:
                                        tokens += [Token("string", str((gch.name)))]
                                    else:
                                        if not vm in self.vars.ins:
                                            return tokens, Error("UndefinedError", "Undefined '" + vm + "'")
                                        if self.vars.ins[vm].name != "section":
                                            return tokens, Error("FunctionError", "Expected 'section' not '" + self.vars.ins[vm].name + "'")
                                        l = self.vars.ins[vm]
                                    
                                        rj = Exe(self.vars.ins[vm].value, self.vars)
                                        if type(rj) == Error:
                                            return tokens, rj
                                        if type(rj) == Token:
                                            tokens += [rj]
                                        else:
                                            tokens += [Token("number", 0)]
                self.pos -= 1
                try:
                    if fn:
                        if self.cfu:
                            self.cfu = False
                        if vm in ['if', 'while', 'for', 'try', 'function', 'return']:
                            if tokens != []:
                                # return tokens, Error("SyntaxError", "Invaild Tokens.")
                                pass
                        tokens += [Token("variable", (vm))]
                        if vm == 'function':
                            self.cfu = True
                    else:
                            pass
                except:
                    pass
            elif char in "+-*/^%":
                tokens += [Token("Operator", char)]
            else:
                return tokens, Error("IllegalCharacter", "'" + char + "'")
        if self.func:
            return tokens, Error("FunctionError", "Unclosed '}'")
        else:

            return tokens, None
class info:
    def __init__(self):
        self.ret = False
        self.vname = None
        self.ref = False
def compile(toks, ins = Instance(), mkvar = False, inf = info(), debug = False):
    if True:
        output = Token()
        pos = 0-1
        op = '*'
        while pos < len(toks)-1:
            pos += 1
            index = toks[pos]
            index: Token
            if index.name == 'Operator':
                op = index.value
            elif index.name == 'number':
                if output.name == '':
                    output.name = 'number'
                    output.value = index.value
                    output.varname = index.varname
                elif output.name == 'number':
                    try:
                        output.value = (eval(repr(output.value) + op + repr(index.value)))*1
                    except:
                        return output
                else:
                    if op == '==':
                        output.name = 'number'
                        output.value = '0'
                    elif op == '!=':
                        output.name = 'number'
                        output.value = '1'
                    else:
                        return Error("UnsupportedError", "Expected '" + output.name + "' not 'number'.")
                op = '*'
            elif index.name == 'string':
                try:
                    if toks[pos+1].name == 'slice':
                        try:
                            u = index.value[toks[pos+1].value]
                            toks[pos+1] = Token("string", u)
                            continue
                        except:
                            return Error("IndexError", "Size " + str(len(index.value)) + ", Prefrenced " + str(toks[pos+1].value) + '.')
                except:
                    pass
                if output.name == '':
                    output.name = 'string'
                    output.value = index.value
                    output.varname = index.varname
                elif output.name == 'string':
                    try:
                        output.value = (eval(repr(output.value) + op + repr(index.value)))
                        if type(output.value) == bool:
                            output.name = 'number'
                            output.value = (output.value) * 1
                    except:
                        return Error("StringError", "Unsupported '" + str(op) + "'")
                else:
                    if op == '==':
                        output.name = 'number'
                        output.value = '0'
                    elif op == '!=':
                        output.name = 'number'
                        output.value = '1'
                    else:
                        return Error("UnsupportedError", "Expected '" + output.name + "' not 'string'.")
                op = '*'
            elif index.name == 'number':
                if output.name == '':
                    output.name = 'number'
                    output.value = index.value
                    output.varname = index.varname
                elif output.name == 'number':
                    try:
                        output.value = (eval(repr(output.value) + op + repr(index.value)))*1
                    except:
                        return output
                else:
                    if op == '==':
                        output.name = 'number'
                        output.value = '0'
                    elif op == '!=':
                        output.name = 'number'
                        output.value = '1'
                    else:
                        return Error("UnsupportedError", "Expected '" + output.name + "' not 'number'.")
                op = '*'
            elif index.name == 'array':
                try:
                    if toks[pos+1].name == 'slice':
                        try:
                            u = index.value[toks[pos+1].value]
                            toks[pos+1] = u
                            continue
                        except:
                            return Error("IndexError", "Size " + str(len(index.value)) + ", Prefrenced " + str(toks[pos+1].value) + '.')
                except:
                    pass
                if output.name == '':
                    output.name = 'array'
                    output.value = index.value
                    output.varname = index.varname
                elif output.name == 'array':
                    try:
                        if not op in ["==", "!=", "+"]:
                
                            return Error("ArrayError", "Unsupported '" + op + "'")
                        else:
                            if op == "+":
                                output.value += index.value
                            if op == '==':
                                output.name = "number"
                                output.value = (output.value == index.name)*1
                            if op == '!=':
                                output.name = "number"
                                output.value = (output.value != index.name)*1
                    except:
                        return Error("StringError", "Unsupported '" + str(op) + "'")
                else:
                    if op == '==':
                        output.name = 'number'
                        output.value = '0'
                    elif op == '!=':
                        output.name = 'number'
                        output.value = '1'
                    else:
                        return Error("UnsupportedError", "Expected '" + output.name + "' not 'array'.")
                op = '*'
            elif index.name == 'variable':
                name = index.value

                if True:
                    try:
                        if toks[pos+1].name == 'ASSIGN':
                            value = compile(toks[pos+2:], ins)
                            value: Token
                            if type(value) == Error:
                                return value
                            ins.ins[name] = value
                            inf.vname = name
                            value.varname = name
                            return value
                            
                    except:
                        pass
                if name == 'if':
                        l = compile([toks[len(toks)-1]], ins)
                        if l.name != 'section':
                            return Error("StatementError", "Expected 'section' not '" + l.name +"'")
                        
                        kmj = compile(toks[pos+1:-1], ins)
                        if type(kmj) == Error:
                            return kmj
                        if kmj.value:
                            k = Exe(l.value, ins)
                            if type(k) == Error:
                                return k
                            if type(k) == Token:
                                inf.ret = True
                                return k
                        return Token("number", "0")
                if name == 'return':
                        sp = compile(toks[pos+1:], ins)
                        if type(sp) == Error:
                            return sp
                        inf.ret = True
                        return sp
                if name == 'function':
                        l = compile([toks[len(toks)-1]], ins)
                        if l.name != 'section':
                            for km in toks:
                                print(km.name, "&",  km.value, "$")
                            return Error("StatementError", "Expected 'section' not '" + l.name +"'")
                        if toks[pos+1].name != "variable":
                            return Error("SyntaxError", "Expected Variable.")
                        if not (len(toks[pos+1:-1]) in [1, 2]):
                            return Error("SyntaxError", "Invaild Tokens.")
                        p = compile(toks[pos+2:-1], ins)
                        if type(p) == Error:
                            return p
                        if p.name != "array":
                            return Error("SyntaxError", "Expected Array Of Values Or Variables")
                        l.args1 = p
                        ins.ins[toks[pos+1].value] = l
                        return Token("number", "0")
                if name == 'try':
                        l = compile(toks[pos+1:], ins)
                        if l.name != 'section':
                            return Error("StatementError", "Expected 'section' not '" + l.name +"'")
                        
                        k = Exe(l.value, ins)
                        if type(k) == Token:
                                inf.ret = True
                                return k
                        return Token("number", "0")
                if name == 'for':
                        l = compile([toks[len(toks)-1]], ins)

                        if l.name != 'section':
                            return Error("StatementError", "Expected 'section' not '" + l.name +"'")

                        infs = info()
                        infs.ref = True
                        kmj = compile(toks[pos+1:-1], ins, False, infs)
                        assign_to = kmj.varname
                        if type(kmj) == Error:
                            return kmj
                        if kmj.name == 'string':
                            for ch in kmj.value:
                                ins.ins[assign_to] = Token("string", ch)
                                k = Exe(l.value, ins)
                                if type(k) == Error:
                                    return k
                                if type(k) == Token:
                                    inf.ret = True
                                    return k
                        elif kmj.name == 'array':
                            for ch in kmj.value:
                                ins.ins[assign_to] = ch
                                k = Exe(l.value, ins)
                                if type(k) == Error:
                                    return k
                                if type(k) == Token:
                                    inf.ret = True
                                    return k
                        elif kmj.name == 'number':
                            for ch in range(eval(str(kmj.value))):
                                ins.ins[assign_to] = Token("number", ch)
                                k = Exe(l.value, ins)
                                if type(k) == Error:
                                    return k
                                if type(k) == Token:
                                    inf.ret = True
                                    return k
                        return Token("number", "0")
                pos -= 1
                try:
                    toks[pos+1] = ins.ins[index.value]
                except:
                    return Error("UndefinedError", "Undefined '"+ index.value + "'")
            elif index.name == 'section':
                if output.name == '':
                    output.name = 'section'
                    output.value = index.value
                    output.argname = index.argname
                    output.args = index.args
                    output.varname = index.varname
                elif output.name == 'section':
                    try:
                        return Error("SectionError", "Cannot Operate")
                    except:
                        return output
                else:
                    return Error("UnsupportedError", "Expected '" + output.name + "' not 'section'.")
    return output

m = True

try:
    content = open(sys.argv[1:][0], "r").read()
except:
    m = False
    print("File Doesn\'t Exists.")

def Exe(text = '', ins = Instance()) -> Instance | Error | Token:
    pos = 0-1
    while pos < len(text)-1:
        
        lexer = Tokenizer(text[pos+1:])
        lexer.vars = ins
        lex = lexer.lex()
        if lex[1] != None:
            err = lex[1]
            err.line = text[0:pos].count("\n")
            return err
        else:
            pass
        pos += lexer.pos+1
        lk = info()
        a = compile(lex[0], ins, inf = lk)
        if type(a) == Error:
            a.line = text[0:pos].count("\n")
            return a
        if lk.ret:
            return a
    return ins

if m:
    try:
        yh = Instance()
        a = Exe(content + "\nmain(0);", yh)
        if type(a) == Error:
            a: Error
            print(a.name + ":", a.value, 'at line', a.line+1)#, 'at line', a.line)
    except:
        pass
