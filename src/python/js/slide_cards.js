let Section = {
    num: 0,
    slide_interval: 0,
    slide_to_section: n=>{
        let cur = Section.num;
        let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        return new Promise((resolve, reject)=>{
            let slide_timeout = setInterval(event=>{
                if (cur<n) {
                    cur = Math.min(cur + 0.00003*vw, n);
                } else if (cur == n) {
                    clearTimeout(slide_timeout);
                    Section.num = n;
                    resolve();
                } else {
                    cur = Math.max(cur - 0.00003*vw, n);
                }
                document.documentElement.style.setProperty("--current-shift", cur);
            }, Section.slide_interval);
        })
    },
    slide_to_next_section: event=>{
        return Section.slide_to_section(Section.num+1);
    },
    slide_to_last_section: event=>{
        return Section.slide_to_section(Section.num-1);
    }

}

App.Section = Section;
