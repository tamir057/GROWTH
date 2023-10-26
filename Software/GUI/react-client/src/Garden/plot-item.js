import React from "react";
const PlotItem = (
 {
   plot = {
     "plotNumber": "1",
     "plant": "Spinach"
   }
 }
) => {
 return(
  <li className="list-group-item bg-secondary-green">
   <div className="row">
     <div className="col-1">
     <input type="checkbox" id="checkbox"></input>
        <button class="m-2 col-3 btn button-square round-15">Plot {plot.plotNumber} {plot.plant} </button>
     </div>
     <div className="col-10 mt-2 ml-0 pl-0">
     {/* <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/>
     <img width={70} height={70} className="float-end" src="/images/hydroponic.png"/> */}


     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>
     <img width={70} height={70} className="float-end" src="/images/garden-plant2.jpg"/>

     </div>
   </div>
  </li>
 );
};
export default PlotItem;