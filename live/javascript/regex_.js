var text = `
My Name is Simon born on 07-10-2002 when the sun was raining
Today is on date 07-06-2023
`

let date_pat = /\b\d{2}-\d{2}-\d{4}\b/gim
let word = /\b[\w-]+\b/gim

export default () => {
    if (date_pat.test(text)) {
        p("Match Found")
        let date = text.match(date_pat)
        p(date)
    }
    let words = text.match(word)
    p(words)
    let t = text.replace(date_pat, "$2")
    p(t)
}