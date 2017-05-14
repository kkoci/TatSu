# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


ANTLR_GRAMMAR = r'''
    (*
        ANTLR v3 grammar written in Tatsu EBNF syntax.

        This grammar is inspired in, but different one by the one created
        by Terence Parr using ANTLR syntax. It is licensed under the BSD
        License to keep in the spirit of ANTLR.
    *)
    
    @@comments :: ?'/\*(?:.|\n)*?\*/'
    @@eol_comments :: ?'//[^\n]*?\n'
    
    start
        =
        grammar
        ;

    grammar
        =
        [('lexer'|'parser')] 'grammar'  name:name ';'
        [options]
        [header]
        [members]
        [imports]
        [tokens]
        {scope}
        {action}
        rules:{rule}+
        $
        ;

    options
        =
        'options'  '{' {option}+ '}' ~
        ;

    option
        =
        id '='   (id|string|char|int|'*') ';' ~
        ;

    imports
        =
        'import'  name {',' name} ';'
        ;

    header
        =
        '@header' block
        ;

    members
        =
        '@members' block
        ;

    tokens
        =
        'tokens'  '{' {token}+ '}'
        ;

    token
        =
        name:token_name ['='  ~ exp:token_value ] ';' ~
        ;

    token_value
        =
        literal
        ;

    scope
        =
        'scope' ~
        (
          block ['scope'  id {',' id} ';' ]
        | id {','  id} ';'
        | id block
        )
        ;

    action
        =
        '@'  ('lexer'|'parser'|id)
        ['::'  id]
        block
        ;

    block
        =
        '{' {block|/[^{}]*/} '}'
        ;

    rule
        =
        ['protected'|'public'|'private'|fragment:'fragment']
        name:id ['!'] [arg]
        ['returns' arg]
        ['trhows' id {',' id}* ]
        [options]
        [scope]
        {action}
        ':'  exp:alternatives ';' ~
        [exceptions]
        ;

    arg
        =
        '[' ~
            {
                arg
            |
                ?/[^\]]*/?
            }*
        ']'
        ;

    exceptions
        =
        {'catch'  arg block}
        ['finally'  block]
        ;

    alternatives
        =
        '|'.{[annotation] options+:alternative}+
        ;

    alternative
        =
        @:elements ['->'  rewrite]
        ;

    elements
        =
        {element}*
        ;

    element
        =
          named
        | predicate_or_action
        | optional
        | closure
        | positive_closure
        | atom
        ;

    named
        =
        name:id (force_list:'+='| '=')   exp:atom
        ;


    predicate_or_action
        =
          gated_predicate
        | semantic_predicate
        | semantic_action
        ;


    gated_predicate
        =
        block '?=>' ~
        ;

    semantic_predicate
        =
        block '?' ~
        ;

    semantic_action
        =
        '{'
            {
                semantic_action
            |
                ?/[^}]/?
            }
        '}'
        ;

    syntactic_predicate
        =
        @:subexp '=>' ~
        ;

    optional
        =
        (
            '(' @:alternatives ')'
        |
            @:(closure|positive_closure|atom)
        )
        '?' ~
        ;

    closure
        =
        @:atom '*' ~
        ;

    positive_closure
        =
        @:atom '+' ~
        ;

    atom
        =
        @:(
        | eof
        | newranges
        | negative
        | regexp
        | syntactic_predicate
        | subexp
        | terminal
        | non_terminal
        )
        ['^'|'!']
        [annotation]
        ;

    annotation
        =
        '<' ','.{id ['=' id]}+ '>'
        ;

    eof
        =
        'EOF'
        ;

    regexp
        =
        {charset}+
        ;


    charset
        =
        | charset_optional
        | charset_closure
        | charset_positive_closure
        | charset_term
        ;


    charset_optional
        =
        '(' @:charset ')' '?' ~
        ;


    charset_closure
        =
        '(' @:charset ')' '*' ~
        ;


    charset_positive_closure
        =
        '(' @:charset ')' '+' ~
        ;


    charset_term
        =
        | '(' @:charset ')'
        | charset_negative_or
        | charset_or
        ;


    charset_or
        =
        | @+:charset_range {'|' @+:charset_atom }
        | @+:charset_char {'|' @+:charset_atom }+
        ;


    charset_negative_or
        =
        '~' '('
            (
            | @+:charset_range {'|' @+:charset_atom }
            | @+:charset_char {'|' @+:charset_atom }+
            )
        ')'
        ;


    charset_atom
        =
        | charset_range
        | char
        ;


    charset_char
        =
        char
        ;


    charset_range
        =
        first:charset_char '..'  last:charset_char
        ;


    newranges
        =
        {negative_newrange|newrange}+
        ;

    newrange
        =
        '['  range:/([^\]]|\\u[a-fA-F0-9]{4}|\\.)+/ ']' repeat:[/[+*?][?]?/]
        ;

    negative_newrange
        =
        '~' '['  range:/([^\]]|\\u[a-fA-F0-9]{4}|\\.)+/ ']' repeat:[/[+*?][?]?/]
        ;


    subexp
        =
        '('
            [options ':' ~ ]
            @:alternatives
        ')'
        ;

    negative
        =
        '~'  @:atom
        ;

    non_terminal
        =
        @:(
          token_ref
        | rule_ref
        )
        [arg]
        ;

    terminal
        =
        | string
        | any
        ;

    any
        =
        !'..' '.' ~
        ;


    rewrite
        =
        {rewrite_term}*
        ;

    rewrite_term
        =
          '^(' {rewrite_term}+ ')'
        | ?/[^|;^)]*/?
        ;

    rule_ref
        =
        lower_name [annotation]
        ;

    token_ref
        =
        upper_name
        ;

    token_name
        =
        upper_name
        ;

    literal
        =
        id | string | int
        ;


    id
        =
        name
        ;

    name
        =
        ?/[a-zA-Z][A-Za-z0-9_]*/?
        ;

    lower_name
        =
        ?/[a-z][A-Za-z0-9_]*/?
        ;

    upper_name
        =
        ?/[A-Z][A-Za-z0-9_]*/?
        ;

    char
        =
        "'"  @:/[^'\n\\]|\\'|\\u[a-fA-F0-9]{4}|\\./ "'"
        ;

    string
        =
        STRING
        ;

    STRING
        =
        '"'  @:/([^"\n\\]|\\u[a-fA-F0-9]{4}|\\['"\\nrtbfv])+/ '"'
        |
        "'"  @:/([^'\n\\]|\\u[a-fA-F0-9]{4}|\\['"\\nrtbfv])+/ "'"
        ;

    int
        =
        /[0-9]+/
        ;

    ESC
        =
        ?/\\['"\\nrtbfv]/?
        |
        ?/\\u[a-fA-F0-9]{4}/?
        ;
'''

