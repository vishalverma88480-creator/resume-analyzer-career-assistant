import { NavLink, Link } from 'react-router-dom';
import { FileText, Menu, X } from 'lucide-react';
import { useState } from 'react';
export default function Navbar(){
 const [open,setOpen]=useState(false);
 const links=[['Home','/'],['Analyze Resume','/upload'],['Career Paths','/career-paths'],['History','/history']];
 return <header className="topbar"><div className="nav-inner"><Link to="/" className="brand" onClick={()=>setOpen(false)}><span className="brand-mark"><FileText size={19}/></span><span>Resume<span className="brand-light">Flow</span></span></Link><button className="mobile-menu" onClick={()=>setOpen(!open)} aria-label="Toggle navigation">{open?<X/>:<Menu/>}</button><nav className={open?'nav-links open':'nav-links'}>{links.map(([label,to])=><NavLink key={to} to={to} end={to==='/'} onClick={()=>setOpen(false)} className={({isActive})=>isActive?'nav-link active':'nav-link'}>{label}</NavLink>)}<Link className="nav-cta" to="/upload" onClick={()=>setOpen(false)}>Analyze resume <span>↗</span></Link></nav></div></header>
}
